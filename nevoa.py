import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0
fog_mode = GL_LINEAR
fog_density = 0.06

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.8, 0.9, 1.0, 1.0)  

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    # luz
    glEnable(GL_LIGHTING); glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (2,3,5,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1,1,1,1))

    # névoa
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR,  (0.8, 0.9, 1.0, 1.0))
    glFogf (GL_FOG_DENSITY, fog_density)
    glFogi(GL_FOG_MODE, fog_mode)      
    glFogf (GL_FOG_START,  5.0)
    glFogf (GL_FOG_END,   25.0)

def cube():
    s=0.6
    glBegin(GL_QUADS)
    glNormal3f(0,0,1);  glVertex3f(-s,-s, s); glVertex3f( s,-s, s); glVertex3f( s, s, s); glVertex3f(-s, s, s)
    glNormal3f(0,0,-1); glVertex3f( s,-s,-s); glVertex3f(-s,-s,-s); glVertex3f(-s, s,-s); glVertex3f( s, s,-s)
    glNormal3f(-1,0,0); glVertex3f(-s,-s,-s); glVertex3f(-s,-s, s); glVertex3f(-s, s, s); glVertex3f(-s, s,-s)
    glNormal3f(1,0,0);  glVertex3f( s,-s, s); glVertex3f( s,-s,-s); glVertex3f( s, s,-s); glVertex3f( s, s, s)
    glNormal3f(0,1,0);  glVertex3f(-s, s, s); glVertex3f( s, s, s); glVertex3f( s, s,-s); glVertex3f(-s, s,-s)
    glNormal3f(0,-1,0); glVertex3f(-s,-s,-s); glVertex3f( s,-s,-s); glVertex3f( s,-s, s); glVertex3f(-s,-s, s)
    glEnd()

def main():
    global angle, fog_mode, fog_density
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Fog (1=LINEAR, 2=EXP, 3=EXP2, ] e [ densidade)")
    init()
    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type==QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                running=False
            if e.type==KEYDOWN and e.key in (K_1, K_2, K_3):
                fog_mode = {K_1:GL_LINEAR, K_2:GL_EXP, K_3:GL_EXP2}[e.key]
                glFogi(GL_FOG_MODE, fog_mode)
            if e.type==KEYDOWN and e.key==K_LEFTBRACKET:
                fog_density = max(0.0, fog_density - 0.01)
                glFogf(GL_FOG_DENSITY, fog_density)
            if e.type==KEYDOWN and e.key==K_RIGHTBRACKET:
                fog_density = min(1.0, fog_density + 0.01)
                glFogf(GL_FOG_DENSITY, fog_density)

        angle += 0.3
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,2,8, 0,0,0, 0,1,0)

        # desenha “corredor” de cubos recuando na névoa
        for i in range(18):
            glPushMatrix()
            glTranslatef((i%3-1)*2.0, (i%2-0.5)*1.1, -i*2.0)
            glRotatef(angle+i*10, 1,1,0)
            glColor3f(0.7, 0.7 - i*0.02, 0.8 - i*0.03)
            cube()
            glPopMatrix()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
