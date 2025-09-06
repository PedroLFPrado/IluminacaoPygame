import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos

angle = 0
culling = True

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.11, 0.11, 0.13, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def torus(R=1.2, r=0.4, ns=48, nt=24):
    # torus para ver faces internas/externas
    for i in range(ns):
        glBegin(GL_QUAD_STRIP)
        for j in range(nt+1):
            for k in (i, i+1):
                s = (k/ns)*2.0*3.14159
                t = (j/nt)*2.0*3.14159
                x = (R + r*cos(t))*cos(s)
                y = (R + r*cos(t))*sin(s)
                z = r*sin(t)
                nx = cos(t)*cos(s)
                ny = cos(t)*sin(s)
                nz = sin(t)
                glNormal3f(nx, ny, nz)
                glVertex3f(x, y, z)
        glEnd()

def main():
    global angle, culling
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Back-Face Culling (toggle: C)")
    init()
    clock = pygame.time.Clock()

    # iluminação leve pra ajudar a perceber o “dentro/fora”
    glEnable(GL_LIGHTING); glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (3,4,5,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1,1,1,1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1,1,1,1))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1,1,1,1))
    glMaterialf(GL_FRONT, GL_SHININESS, 40)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type==QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                running = False
            if e.type==KEYDOWN and e.key==K_c:
                culling = not culling
                if culling:
                    glEnable(GL_CULL_FACE); glCullFace(GL_BACK)
                else:
                    glDisable(GL_CULL_FACE)

        angle += 0.5
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,0,6, 0,0,0, 0,1,0)
        glRotatef(angle, 0,1,0)
        glColor3f(0.8, 0.8, 0.9)
        torus()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
