import math, pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0

def init():
    glEnable(GL_DEPTH_TEST)              # Z-buffer ligado (Hidden-Surface Removal)
    glClearColor(0.1, 0.1, 0.12, 1.0)
    glEnable(GL_CULL_FACE)              
    glCullFace(GL_BACK)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def cube(size=1.0):
    s = size/2
    # 6 faces do cubo
    faces = [
        # frente
        ([[-s,-s, s],[ s,-s, s],[ s, s, s],[-s, s, s]], [0,0,1]),
        # trás
        ([[ s,-s,-s],[-s,-s,-s],[-s, s,-s],[ s, s,-s]],[0,0,-1]),
        # esquerda
        ([[-s,-s,-s],[-s,-s, s],[-s, s, s],[-s, s,-s]],[-1,0,0]),
        # direita
        ([[ s,-s, s],[ s,-s,-s],[ s, s,-s],[ s, s, s]], [1,0,0]),
        # topo
        ([[-s, s, s],[ s, s, s],[ s, s,-s],[-s, s,-s]],[0,1,0]),
        # base
        ([[-s,-s,-s],[ s,-s,-s],[ s,-s, s],[-s,-s, s]],[0,-1,0]),
    ]
    glBegin(GL_QUADS)
    for quad, n in faces:
        glNormal3fv(n)
        for vx in quad:
            glVertex3fv(vx)
    glEnd()

def main():
    global angle
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Z-Buffer & Hidden-Surface Removal")
    init()
    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                running = False

        angle += 0.6
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,2,7, 0,0,0, 0,1,0)

        # cubo 1 (vermelho)
        glPushMatrix()
        glTranslatef(-0.7, 0, 0)
        glRotatef(angle, 0,1,0)
        glColor3f(0.9, 0.2, 0.2)
        cube(2.0)
        glPopMatrix()

        # cubo 2 (azul)
        glPushMatrix()
        glTranslatef(0.7, 0, 0)
        glRotatef(-angle*1.2, 1,1,0)
        glColor3f(0.2, 0.4, 0.9)
        cube(2.0)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
