import math
import random
import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import pygame

from src.content import (
    BOSSES,
    ENEMY_ARCHETYPES,
    MAIN_LORE,
    MINIBOSSES,
    RANDOM_EVENTS,
    SKILL_TREE,
    UNIQUE_ITEMS,
)

WIDTH, HEIGHT = 1100, 640
GRAVITY = 0.6
GROUND_Y = HEIGHT - 80
WHITE = (245, 245, 245)
BLACK = (15, 15, 15)
RED = (170, 40, 40)
BLUE = (70, 120, 210)
GREEN = (60, 170, 100)
PURPLE = (130, 70, 170)
ORANGE = (220, 130, 40)


@dataclass
class Stats:
    max_hp: int = 100
    hp: int = 100
    atk: int = 12
    defense: int = 2
    speed: float = 5.5
    crit: float = 0.08
    max_jumps: int = 2


class SkillTree:
    def __init__(self):
        self.nodes = SKILL_TREE
        self.unlocked = {"embers_of_will"}
        self.points = 3

    def unlocked_nodes(self):
        return [self.nodes[k] for k in self.unlocked]

    def can_unlock(self, key: str) -> bool:
        node = self.nodes.get(key)
        if not node or key in self.unlocked:
            return False
        if self.points < node["cost"]:
            return False
        return all(req in self.unlocked for req in node["requires"])

    def unlock(self, key: str, stats: Stats):
        if not self.can_unlock(key):
            return False
        node = self.nodes[key]
        self.points -= node["cost"]
        self.unlocked.add(key)
        for stat, value in node["effects"].items():
            current = getattr(stats, stat)
            setattr(stats, stat, current + value)
        stats.hp = min(stats.hp, stats.max_hp)
        return True


@dataclass
class Item:
    name: str
    rarity: str
    kind: str
    effect: Dict[str, float]


class Inventory:
    def __init__(self, cap: int = 24):
        self.capacity = cap
        self.items: List[Item] = []

    def add(self, item: Item) -> bool:
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove(self, idx: int) -> Optional[Item]:
        if 0 <= idx < len(self.items):
            return self.items.pop(idx)
        return None

    def use_item(self, idx: int, player: "Player"):
        item = self.remove(idx)
        if not item:
            return
        for stat, val in item.effect.items():
            if stat == "heal":
                player.stats.hp = min(player.stats.max_hp, int(player.stats.hp + val))
            elif hasattr(player.stats, stat):
                setattr(player.stats, stat, getattr(player.stats, stat) + val)


class Entity:
    def __init__(self, x: float, y: float, w: int, h: int, color, hp=20):
        self.rect = pygame.Rect(int(x), int(y), w, h)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.on_ground = False
        self.dead = False
        self.facing = 1
        self.invuln_timer = 0

    def physics(self, platforms):
        self.vel_y += GRAVITY
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        for p in platforms:
            if self.rect.colliderect(p) and self.vel_y >= 0 and self.rect.bottom - self.vel_y <= p.top + 8:
                self.rect.bottom = p.top
                self.vel_y = 0
                self.on_ground = True

        if self.invuln_timer > 0:
            self.invuln_timer -= 1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        hp_w = self.rect.w
        ratio = max(0, self.hp) / self.max_hp if self.max_hp else 0
        pygame.draw.rect(surf, RED, (self.rect.x, self.rect.y - 8, hp_w, 5))
        pygame.draw.rect(surf, GREEN, (self.rect.x, self.rect.y - 8, int(hp_w * ratio), 5))

    def take_damage(self, amt: int):
        if self.invuln_timer > 0:
            return
        self.hp -= amt
        self.invuln_timer = 18
        if self.hp <= 0:
            self.dead = True


class Player(Entity):
    def __init__(self):
        super().__init__(120, 200, 40, 56, BLUE, 100)
        self.stats = Stats()
        self.jump_count = 0
        self.attack_cd = 0
        self.dash_cd = 0
        self.inventory = Inventory()
        self.skill_tree = SkillTree()
        self.souls = 0

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -self.stats.speed
            self.facing = -1
        if keys[pygame.K_d]:
            self.vel_x = self.stats.speed
            self.facing = 1

    def jump(self):
        if self.jump_count < self.stats.max_jumps:
            self.vel_y = -11.5
            self.jump_count += 1

    def dash(self):
        if self.dash_cd <= 0:
            self.vel_x = 16 * self.facing
            self.dash_cd = 90

    def attack_rect(self):
        if self.facing == 1:
            return pygame.Rect(self.rect.right, self.rect.y + 12, 30, 30)
        return pygame.Rect(self.rect.left - 30, self.rect.y + 12, 30, 30)

    def attack_damage(self):
        dmg = self.stats.atk
        if random.random() <= self.stats.crit:
            dmg = int(dmg * 1.8)
        return dmg

    def physics(self, platforms):
        super().physics(platforms)
        if self.on_ground:
            self.jump_count = 0
        if self.attack_cd > 0:
            self.attack_cd -= 1
        if self.dash_cd > 0:
            self.dash_cd -= 1


class Enemy(Entity):
    def __init__(self, x, y, profile):
        super().__init__(x, y, 36, 48, ORANGE, profile["hp"])
        self.profile = profile
        self.name = profile["name"]
        self.moveset = profile["moveset"]
        self.speed = profile["speed"]
        self.cooldown = random.randint(20, 120)
        self.pattern_timer = 0
        self.phase = 1

    def update(self, player, platforms):
        if self.dead:
            return
        self.pattern_timer += 1
        move = self.profile["ai"](self, player)

        if move == "stalk":
            self.vel_x = self.speed if player.rect.centerx > self.rect.centerx else -self.speed
        elif move == "hop" and self.on_ground:
            self.vel_y = -9
        elif move == "dash":
            self.vel_x = 8 if player.rect.centerx > self.rect.centerx else -8
        elif move == "retreat":
            self.vel_x = -self.speed if player.rect.centerx > self.rect.centerx else self.speed
        else:
            self.vel_x *= 0.86

        if self.rect.colliderect(player.rect.inflate(20, 10)) and self.cooldown <= 0:
            dmg = max(1, self.profile["damage"] - player.stats.defense)
            player.take_damage(dmg)
            self.cooldown = 70
        self.cooldown -= 1

        if self.max_hp > 170 and self.hp < self.max_hp // 2:
            self.phase = 2
            self.speed += 0.005

        super().physics(platforms)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ashbound: Escape from Hell")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big = pygame.font.SysFont("consolas", 34)

        self.player = Player()
        self.platforms = [
            pygame.Rect(140, 460, 260, 20),
            pygame.Rect(520, 380, 220, 20),
            pygame.Rect(840, 290, 180, 20),
            pygame.Rect(380, 260, 190, 20),
        ]
        self.wave = 1
        self.depth = 0
        self.stage = "regular"
        self.enemies: List[Enemy] = []
        self.log: List[str] = [MAIN_LORE[0]]
        self.spawn_wave()

    def spawn_wave(self):
        self.enemies.clear()
        if self.wave % 5 == 0:
            self.stage = "boss"
            boss_key = list(BOSSES.keys())[(self.wave // 5 - 1) % len(BOSSES)]
            self.enemies.append(Enemy(830, 160, BOSSES[boss_key]))
            self.log.append(f"Boss Approaches: {BOSSES[boss_key]['name']}")
        elif self.wave % 3 == 0:
            self.stage = "miniboss"
            mini_key = list(MINIBOSSES.keys())[(self.wave // 3 - 1) % len(MINIBOSSES)]
            self.enemies.append(Enemy(760, 170, MINIBOSSES[mini_key]))
            self.log.append(f"Mini-boss: {MINIBOSSES[mini_key]['name']}")
            for _ in range(2):
                profile = random.choice(list(ENEMY_ARCHETYPES.values()))
                self.enemies.append(Enemy(random.randint(500, 960), 120, profile))
        else:
            self.stage = "regular"
            for _ in range(4 + self.wave // 2):
                profile = random.choice(list(ENEMY_ARCHETYPES.values()))
                self.enemies.append(Enemy(random.randint(300, 980), 100, profile))

    def reward_loot(self):
        count = 2 if self.stage == "regular" else 4
        for _ in range(count):
            raw = random.choice(UNIQUE_ITEMS)
            self.player.inventory.add(Item(raw["name"], raw["rarity"], raw["type"], raw["effect"]))

    def apply_random_event(self):
        event = random.choice(RANDOM_EVENTS)
        self.log.append(f"Event: {event['name']} - {event['text']}")
        event["effect"](self)

    def next_wave(self):
        self.wave += 1
        self.depth += 1
        self.player.skill_tree.points += 1
        self.reward_loot()
        if self.wave % 2 == 0:
            self.apply_random_event()
        self.spawn_wave()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_LSHIFT:
                    self.player.dash()
                elif event.key == pygame.K_j and self.player.attack_cd <= 0:
                    atk_box = self.player.attack_rect()
                    for e in self.enemies:
                        if not e.dead and atk_box.colliderect(e.rect):
                            e.take_damage(self.player.attack_damage())
                    self.player.attack_cd = 22
                elif event.key == pygame.K_i and self.player.inventory.items:
                    self.player.inventory.use_item(0, self.player)
                elif event.key == pygame.K_u:
                    unlockable = [k for k in SKILL_TREE.keys() if self.player.skill_tree.can_unlock(k)]
                    if unlockable:
                        self.player.skill_tree.unlock(unlockable[0], self.player.stats)

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.physics(self.platforms)

        for e in self.enemies:
            e.update(self.player, self.platforms)

        for e in self.enemies:
            if e.dead:
                self.player.souls += 10

        self.enemies = [e for e in self.enemies if not e.dead]

        if not self.enemies:
            self.next_wave()

    def draw_ui(self):
        pygame.draw.rect(self.screen, (30, 20, 20), (0, HEIGHT - 80, WIDTH, 80))
        hp_txt = self.font.render(f"HP: {self.player.stats.hp}/{self.player.stats.max_hp}", True, WHITE)
        souls = self.font.render(f"Souls: {self.player.souls}", True, WHITE)
        wave = self.font.render(f"Wave {self.wave} ({self.stage})", True, WHITE)
        pts = self.font.render(f"Skill Points: {self.player.skill_tree.points} (U unlock)", True, WHITE)
        inv = self.font.render(f"Inventory: {len(self.player.inventory.items)}/{self.player.inventory.capacity} (I use slot 1)", True, WHITE)

        self.screen.blit(hp_txt, (20, HEIGHT - 72))
        self.screen.blit(souls, (20, HEIGHT - 48))
        self.screen.blit(wave, (300, HEIGHT - 72))
        self.screen.blit(pts, (300, HEIGHT - 48))
        self.screen.blit(inv, (700, HEIGHT - 60))

        lore = self.font.render(self.log[-1][-74:], True, (230, 210, 170))
        self.screen.blit(lore, (20, 12))

        if self.player.attack_cd > 0:
            a = self.player.attack_rect()
            pygame.draw.rect(self.screen, PURPLE, a, 2)

    def render(self):
        self.screen.fill((18, 12, 14))
        for p in self.platforms:
            pygame.draw.rect(self.screen, (88, 76, 71), p)

        self.player.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)

        self.draw_ui()
        pygame.display.flip()

    def run(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    intro = False
            self.screen.fill(BLACK)
            title = self.big.render("ASHBOUND: FIGHT OUT OF HELL", True, RED)
            subtitle = self.font.render("Move A/D | Jump Space | Dash Shift | Attack J | Inventory I | Skill U", True, WHITE)
            lore = self.font.render(MAIN_LORE[1], True, WHITE)
            self.screen.blit(title, (180, 250))
            self.screen.blit(subtitle, (120, 320))
            self.screen.blit(lore, (80, 360))
            pygame.display.flip()
            self.clock.tick(30)

        while True:
            self.handle_events()
            self.update()
            self.render()
            if self.player.dead:
                pygame.quit()
                return
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
