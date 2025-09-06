import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0
smooth = True
mat_mode = 2

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.12, 0.12, 0.14, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.15,0.15,0.15,1.0))
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)

    # luz principal
    glEnable(GL_LIGHTING); glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (3, 4, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

def apply_material(mode):
    if mode == 1:  # fosco
        glMaterialfv(GL_FRONT, GL_AMBIENT,  (0.2,0.2,0.2,1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE,  (0.6,0.3,0.2,1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0,0.0,0.0,1))
        glMaterialf (GL_FRONT, GL_SHININESS, 1)
    elif mode == 2:  # plástico
        glMaterialfv(GL_FRONT, GL_AMBIENT,  (0.1,0.1,0.1,1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE,  (0.2,0.5,0.8,1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.9,0.9,0.9,1))
        glMaterialf (GL_FRONT, GL_SHININESS, 40)
    else:  # metal
        glMaterialfv(GL_FRONT, GL_AMBIENT,  (0.25,0.22,0.22,1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE,  (0.35,0.35,0.35,1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.9,0.9,0.9,1))
        glMaterialf (GL_FRONT, GL_SHININESS, 90)

def sphere(radius=1.5, slices=48, stacks=32):
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    gluDeleteQuadric(q)

def main():
    global angle, smooth, mat_mode
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Iluminacao: Shading, Materiais, Modelo e Luz (G/1/2/3)")
    init()
    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type==QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                running=False
            if e.type==KEYDOWN and e.key==K_g:
                smooth = not smooth
                glShadeModel(GL_SMOOTH if smooth else GL_FLAT)
            if e.type==KEYDOWN and e.key in (K_1, K_2, K_3):
                mat_mode = {K_1:1, K_2:2, K_3:3}[e.key]

        angle += 0.5
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,1.5,6, 0,0,0, 0,1,0)

        apply_material(mat_mode)
        glRotatef(angle, 0,1,0)
        sphere()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
