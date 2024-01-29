import pygame
import sys
import random
import math
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
# Initialize Pygame
pygame.init()
pygame.mixer.init()
# collide = pygame.mixer.Sound('hit.wav')

# Constants
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 240

# Colors
GREY = (50, 69, 69, 255)
RED = (0, 0, 0, 1)
WHITE = (255, 255, 255, 1)
BLACK = (0, 0, 0)

# Circle properties
outer_radius = 350
inner_radius = 25
inner_radius2 = 25
angular_speed = 0.05
angular_speed2 = 0.05
gravity = 0.04
central_gravity = 0.05
central_radius = 100

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Increased height for buttons
pygame.display.set_caption("Rolling Circles")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.Font(None, 36)


def generate_color():
    # Adjust the parameters to control the color change speed and range
    time_factor = pygame.time.get_ticks() / 100.0  # Convert milliseconds to seconds
    r = int(127 + 127 * math.sin(0.5 * time_factor))
    g = int(127 + 127 * math.sin(0.5 * time_factor + 2))
    b = int(127 + 127 * math.sin(0.5 * time_factor + 4))
    a = int(1)
    return (r, g, b, a)


def generate_color1():
    # Adjust the parameters to control the color change speed and range
    time_factor = pygame.time.get_ticks() / 100.0  # Convert milliseconds to seconds
    r = int(127 + 127 * math.sin(0.5 * time_factor))
    g = int(127 + 127 * math.sin(0.5 * time_factor - 2))
    b = int(127 + 127 * math.sin(0.5 * time_factor - 4))
    a = int(1)
    return (r, g, b, a)


def generate_gray():
    # Adjust the parameters to control the color change speed and range
    time_factor = pygame.time.get_ticks() / 100.0  # Convert milliseconds to seconds
    r = int(127 + 127 * math.sin(0.5 * time_factor))
    g = int(127 + 127 * math.sin(0.5 * time_factor))
    b = int(127 + 127 * math.sin(0.5 * time_factor))
    a = int(1)
    return (r, g, b, a)


def generate_gray1():
    # Adjust the parameters to control the color change speed and range
    time_factor = pygame.time.get_ticks() / 100.0  # Convert milliseconds to seconds
    r = int(127 + 127 * math.sin(0.5 * time_factor - 2))
    g = int(127 + 127 * math.sin(0.5 * time_factor - 2))
    b = int(127 + 127 * math.sin(0.5 * time_factor - 2))
    a = int(1)
    return (r, g, b, a)


# Function to draw the circles
def draw_circles(inner_pos, angle, trail):
    # Draw ghost trail with tapered size
    for i, pos in enumerate(trail):
        size_multiplier = i / len(trail)  # Corrected taper direction
        size = int(inner_radius * (0.1 + size_multiplier))
        pygame.draw.circle(screen, generate_gray(), (int(pos[0]), int(pos[1])), size)

    # Draw inner circle
    pygame.draw.circle(screen, generate_gray1(), inner_pos, inner_radius)

    for i, pos in enumerate(trail):
        size_multiplier = i / len(trail)  # Corrected taper direction
        size2 = int(inner_radius * (0.05 + size_multiplier))
        pygame.draw.circle(screen, generate_gray1(), (int(pos[0]), int(pos[1])), size2)

    # Draw line indicating angular movement
    end_point = (inner_pos[0] + inner_radius * math.cos(angle),
                 inner_pos[1] + inner_radius * math.sin(angle))
    pygame.draw.line(screen, generate_gray1(), inner_pos, end_point, 2)


def draw_circles2(inner_pos2, angle2, trail2):

    # Draw ghost trail with tapered size
    for i, pos in enumerate(trail2):
        size_multiplier = i / len(trail2)  # Corrected taper direction
        size3 = int(inner_radius2 * (0.1 + size_multiplier))
        pygame.draw.circle(screen, generate_color(), (int(pos[0]), int(pos[1])), size3)

    # Draw inner circle
    pygame.draw.circle(screen, generate_color(), inner_pos2, inner_radius2)

    for i, pos in enumerate(trail2):
        size_multiplier = i / len(trail2)  # Corrected taper direction
        size4 = int(inner_radius2 * (0.05 + size_multiplier))
        pygame.draw.circle(screen, generate_color1(), (int(pos[0]), int(pos[1])), size4)

    # Draw line indicating angular movement
    end_point2 = (inner_pos2[0] + inner_radius2 * math.cos(angle2),
                  inner_pos2[1] + inner_radius2 * math.sin(angle2))
    pygame.draw.line(screen, generate_color1(), inner_pos2, end_point2, 2)


def calculate_gravitational_force(point1, point2, strength):
    direction = [point2[0] - point1[0], point2[1] - point1[1]]
    distance_squared = direction[0] ** 2 + direction[1] ** 2
    distance = math.sqrt(distance_squared)

    if distance == 0:
        return [0, 0]

    force_magnitude = strength / distance_squared
    force = [force_magnitude * direction[0] / distance, force_magnitude * direction[1] / distance]

    return force


def draw_central_circle(central_pos):
    pygame.draw.circle(screen, WHITE, central_pos, central_radius)


# Function to check if the inner circle is inside the outer circle
def is_inside_outer_circle(inner_pos):
    distance = math.sqrt((inner_pos[0] - WIDTH // 2) ** 2 + (inner_pos[1] - HEIGHT // 2) ** 2)
    return distance + inner_radius <= outer_radius


def is_inside_outer_circle2(inner_pos2):
    distance = math.sqrt((inner_pos2[0] - WIDTH // 2) ** 2 + (inner_pos2[1] - HEIGHT // 2) ** 2)
    return distance + inner_radius2 <= outer_radius


# Function to draw buttons
def draw_buttons():
    pygame.draw.rect(screen, WHITE, gravity_minus_button)
    pygame.draw.rect(screen, WHITE, gravity_plus_button)
    pygame.draw.rect(screen, WHITE, inner_radius_minus_button)
    pygame.draw.rect(screen, WHITE, inner_radius_plus_button)
    pygame.draw.rect(screen, WHITE, outer_radius_minus_button)
    pygame.draw.rect(screen, WHITE, outer_radius_plus_button)
    pygame.draw.rect(screen, WHITE, trail_size_minus_button)
    pygame.draw.rect(screen, WHITE, trail_size_plus_button)

    # Draw button labels
    gravity_minus_label = font.render("-", True, BLACK)
    gravity_plus_label = font.render("+", True, BLACK)
    inner_radius_minus_label = font.render("-", True, BLACK)
    inner_radius_plus_label = font.render("+", True, BLACK)
    outer_radius_minus_label = font.render("-", True, BLACK)
    outer_radius_plus_label = font.render("+", True, BLACK)
    trail_size_minus_label = font.render("-", True, BLACK)
    trail_size_plus_label = font.render("+", True, BLACK)

    screen.blit(gravity_minus_label, (gravity_minus_button.x + 7, gravity_minus_button.y + 5))
    screen.blit(gravity_plus_label, (gravity_plus_button.x + 7, gravity_plus_button.y + 5))
    screen.blit(inner_radius_minus_label, (inner_radius_minus_button.x + 7, inner_radius_minus_button.y + 5))
    screen.blit(inner_radius_plus_label, (inner_radius_plus_button.x + 7, inner_radius_plus_button.y + 5))
    screen.blit(outer_radius_minus_label, (outer_radius_minus_button.x + 7, outer_radius_minus_button.y + 5))
    screen.blit(outer_radius_plus_label, (outer_radius_plus_button.x + 7, outer_radius_plus_button.y + 5))
    screen.blit(trail_size_minus_label, (trail_size_minus_button.x + 7, trail_size_minus_button.y + 5))
    screen.blit(trail_size_plus_label, (trail_size_plus_button.x + 7, trail_size_plus_button.y + 5))

    # Draw current values
    gravity_value_text = font.render(f"Gravity: {gravity:.2f}", True, WHITE)
    inner_radius_value_text = font.render(f"Inner Radius: {inner_radius}", True, WHITE)
    outer_radius_value_text = font.render(f"Outer Radius: {outer_radius}", True, WHITE)
    trail_size_value_text = font.render(f"Trail Size: {trail_size_value:.2f}", True, WHITE)

    screen.blit(gravity_value_text, (220, HEIGHT - 50))
    screen.blit(inner_radius_value_text, (220, HEIGHT - 90))
    screen.blit(outer_radius_value_text, (220, HEIGHT - 130))
    screen.blit(trail_size_value_text, (220, HEIGHT - 170))


# Function to calculate the reflection vector
def reflect(incident, normal):
    dot_product = 2 * (incident[0] * normal[0] + incident[1] * normal[1])
    return [incident[0] - dot_product * normal[0], incident[1] - dot_product * normal[1]]


# Main game loop
running = True
inner_pos = [WIDTH // 2, HEIGHT // 2]
angle = 0.0
inner_velocity = [random.choice([-1, 1]) * 1.0,
                  random.choice([-1, 1]) * 1.0]

inner_pos2 = [WIDTH // 1.5, HEIGHT // 2 - outer_radius + inner_radius2]
angle2 = 0.0
inner_velocity2 = [0.0, 1.0]
central_pos = [WIDTH // 2, HEIGHT // 2]
ghost_trail = []
ghost_trail2 = []

# Buttons
gravity_minus_button = pygame.Rect(10, HEIGHT - 50, 30, 30)
gravity_plus_button = pygame.Rect(50, HEIGHT - 50, 30, 30)
inner_radius_minus_button = pygame.Rect(10, HEIGHT - 90, 30, 30)
inner_radius_plus_button = pygame.Rect(50, HEIGHT - 90, 30, 30)
outer_radius_minus_button = pygame.Rect(10, HEIGHT - 130, 30, 30)
outer_radius_plus_button = pygame.Rect(50, HEIGHT - 130, 30, 30)
trail_size_minus_button = pygame.Rect(10, HEIGHT - 170, 30, 30)
trail_size_plus_button = pygame.Rect(50, HEIGHT - 170, 30, 30)

trail_size_value = 1.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Gravity buttons
            if gravity_minus_button.collidepoint(mouse_x, mouse_y):
                gravity -= 0.01
            elif gravity_plus_button.collidepoint(mouse_x, mouse_y):
                gravity += 0.01

            # Inner Radius buttons
            elif inner_radius_minus_button.collidepoint(mouse_x, mouse_y):
                inner_radius = max(5, inner_radius - 5)
                inner_radius2 = max(5, inner_radius2 - 5)
            elif inner_radius_plus_button.collidepoint(mouse_x, mouse_y):
                inner_radius += 5
                inner_radius2 += 5

            # Outer Radius buttons
            elif outer_radius_minus_button.collidepoint(mouse_x, mouse_y):
                outer_radius = max(inner_radius + 5, outer_radius - 5)
            elif outer_radius_plus_button.collidepoint(mouse_x, mouse_y):
                outer_radius += 5

            # Trail Size buttons
            elif trail_size_minus_button.collidepoint(mouse_x, mouse_y):
                trail_size_value = max(0.1, trail_size_value - 0.1)
            elif trail_size_plus_button.collidepoint(mouse_x, mouse_y):
                trail_size_value = min(10.0, trail_size_value + 0.1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    # Update inner circle position, velocity, and angle
    inner_velocity[1] += gravity
    inner_pos[0] += inner_velocity[0]
    inner_pos[1] += inner_velocity[1]
    angle += angular_speed

    inner_velocity2[1] += gravity
    inner_pos2[0] += inner_velocity2[0]
    inner_pos2[1] += inner_velocity2[1]
    angle2 += angular_speed2

    # Update central circle position
    central_force1 = calculate_gravitational_force(inner_pos, central_pos, central_gravity)
    central_force2 = calculate_gravitational_force(inner_pos2, central_pos, central_gravity)

    inner_velocity[0] += central_force1[0]
    inner_velocity[1] += central_force1[1]

    inner_velocity2[0] += central_force2[0]
    inner_velocity2[1] += central_force2[1]

    # Collision detection and response for circle1 and ghost_trail2
    for i, pos in enumerate(ghost_trail2):
        distance_to_point = math.sqrt((inner_pos[0] - pos[0]) ** 2 + (inner_pos[1] - pos[1]) ** 2)

        if distance_to_point < inner_radius + int(inner_radius * (0.1 + i / len(ghost_trail))):
            normal = [inner_pos[0] - pos[0], inner_pos[1] - pos[1]]
            normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            if normal_length != 0:
                normal = [normal[0] / normal_length, normal[1] / normal_length]
                inner_velocity = reflect(inner_velocity, normal)
            # collide.play()

    # Collision detection and response for circle2 and ghost_trail
    for i, pos in enumerate(ghost_trail):
        distance_to_point = math.sqrt((inner_pos2[0] - pos[0]) ** 2 + (inner_pos2[1] - pos[1]) ** 2)

        if distance_to_point < inner_radius2 + int(inner_radius2 * (0.1 + i / len(ghost_trail2))):
            normal2 = [inner_pos2[0] - pos[0], inner_pos2[1] - pos[1]]
            normal_length2 = math.sqrt(normal2[0] ** 2 + normal2[1] ** 2)
            if normal_length2 != 0:
                normal2 = [normal2[0] / normal_length2, normal2[1] / normal_length2]
                inner_velocity2 = reflect(inner_velocity2, normal2)
            # collide.play()

    # Bounce off the walls of the outer circle
    if not is_inside_outer_circle(inner_pos):
        angle = math.atan2(inner_pos[1] - HEIGHT // 2, inner_pos[0] - WIDTH // 2)
        inner_pos[0] = int((outer_radius - inner_radius) * math.cos(angle)) + WIDTH // 2
        inner_pos[1] = int((outer_radius - inner_radius) * math.sin(angle)) + HEIGHT // 2
        normal = [inner_pos[0] - WIDTH // 2, inner_pos[1] - HEIGHT // 2]
        normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
        if normal_length != 0:
            normal = [normal[0] / normal_length, normal[1] / normal_length]
            inner_velocity = reflect(inner_velocity, normal)
        # collide.play()

    if not is_inside_outer_circle(inner_pos2):
        angle2 = math.atan2(inner_pos2[1] - HEIGHT // 2, inner_pos2[0] - WIDTH // 2)
        inner_pos2[0] = int((outer_radius - inner_radius2) * math.cos(angle2)) + WIDTH // 2
        inner_pos2[1] = int((outer_radius - inner_radius2) * math.sin(angle2)) + HEIGHT // 2
        normal2 = [inner_pos2[0] - WIDTH // 2, inner_pos2[1] - HEIGHT // 2]
        normal_length2 = math.sqrt(normal2[0] ** 2 + normal2[1] ** 2)
        if normal_length2 != 0:
            normal2 = [normal2[0] / normal_length2, normal2[1] / normal_length2]
            inner_velocity2 = reflect(inner_velocity2, normal2)
        # collide.play()

    distance_between_balls = math.sqrt((inner_pos2[0] - inner_pos[0]) ** 2 + (inner_pos2[1] - inner_pos[1]) ** 2)
    if distance_between_balls < inner_radius + inner_radius2:
        # Balls have collided
        relative_velocity = [inner_velocity2[0] - inner_velocity[0], inner_velocity2[1] - inner_velocity[1]]
        normal_collision = [inner_pos2[0] - inner_pos[0], inner_pos2[1] - inner_pos[1]]
        normal_length_collision = math.sqrt(normal_collision[0] ** 2 + normal_collision[1] ** 2)
        normal_collision = [normal_collision[0] / normal_length_collision,
                            normal_collision[1] / normal_length_collision]

        # Reflect velocities
        inner_velocity = [v + normal_collision[i] * 2.5 for i, v in enumerate(inner_velocity)]
        inner_velocity2 = [v + normal_collision[i] * 2.5 for i, v in enumerate(inner_velocity2)]
        # collide.play()

    # Fill the background
    screen.fill(BLACK)
    outer_circle_color = generate_color()
    pygame.draw.circle(screen, GREY, (WIDTH // 2, HEIGHT // 2), outer_radius)

    # Add current position to the ghost trail
    ghost_trail.append(list(inner_pos))
    if len(ghost_trail) > int(50 * trail_size_value):
        ghost_trail.pop(0)

    ghost_trail2.append(list(inner_pos2))
    if len(ghost_trail2) > int(50 * trail_size_value):
        ghost_trail2.pop(0)

    # Draw circles
    draw_circles(inner_pos, angle, ghost_trail)
    draw_circles2(inner_pos2, angle2, ghost_trail2)

    # Draw buttons
    draw_buttons()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
