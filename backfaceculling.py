import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Vértices do cubo
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Faces do cubo
faces = [
    (0, 1, 2, 3),  # trás
    (4, 5, 6, 7),  # frente
    (0, 1, 5, 4),  # direita
    (2, 3, 7, 6),  # esquerda
    (0, 3, 7, 4),  # cima
    (1, 2, 6, 5)   # baixo
]

# Cores diferentes para cada face
colors = [
    (1, 0, 0),  # vermelho
    (0, 1, 0),  # verde
    (0, 0, 1),  # azul
    (1, 1, 0),  # amarelo
    (1, 0, 1),  # magenta
    (0, 1, 1)   # ciano
]

def draw_cube():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)  # culling
    glCullFace(GL_BACK)     # começa eliminando faces de trás
    glFrontFace(GL_CCW)     # ordem dos vértices: anti-horário

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    cull_modes = [GL_BACK, GL_FRONT, GL_FRONT_AND_BACK]
    cull_names = ["GL_BACK", "GL_FRONT", "GL_FRONT_AND_BACK"]
    current_mode = 0

    pygame.display.set_caption(f"Culling: {cull_names[current_mode]}")

    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_c:  # troca o modo de culling
                    current_mode = (current_mode + 1) % len(cull_modes)
                    glCullFace(cull_modes[current_mode])
                    pygame.display.set_caption(f"Culling: {cull_names[current_mode]}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle, 1, 1, 0)
        draw_cube()
        glPopMatrix()

        angle += 1

        pygame.display.flip()
        pygame.time.wait(20)

    pygame.quit()

if __name__ == "__main__":
    main()
