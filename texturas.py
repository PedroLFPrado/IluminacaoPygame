import os, pygame, numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0
use_linear = True
tex_id = None

def make_checker(size=256, checks=8):
    """Gera textura xadrez caso 'crate.jpg' não exista"""
    img = np.zeros((size, size, 3), dtype=np.uint8)
    step = size // checks
    for y in range(size):
        for x in range(size):
            c = 255 if ((x//step + y//step) % 2) == 0 else 60
            img[y, x] = (c, c, c)
    return img

def load_texture():
    global tex_id
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    path = "crate.jpg"
    if os.path.exists(path):
        surf = pygame.image.load(path)
        img = pygame.image.tostring(surf, "RGB", True)
        w, h = surf.get_rect().size
    else:
        arr = make_checker()
        img = arr.tobytes()
        w, h = arr.shape[1], arr.shape[0]

    # Define parâmetros de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    # Cria textura base e gera mipmaps automaticamente
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glGenerateMipmap(GL_TEXTURE_2D)

    set_filters()

def set_filters():
    """Alterna filtros para ver diferença no mipmapping"""
    min_f = GL_LINEAR_MIPMAP_LINEAR if use_linear else GL_NEAREST_MIPMAP_NEAREST
    mag_f = GL_LINEAR if use_linear else GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_f)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, mag_f)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glClearColor(0.09, 0.09, 0.11, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    # Luz simples
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (2,3,4,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1,1,1,1))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.6,0.6,0.6,1))
    glMaterialf(GL_FRONT, GL_SHININESS, 32)

    # Habilita texturas
    glEnable(GL_TEXTURE_2D)
    load_texture()

def textured_cube(s=1.5):
    """Cubo com coordenadas de textura"""
    glBegin(GL_QUADS)
    # frente
    glNormal3f(0,0,1)
    glTexCoord2f(0,0); glVertex3f(-s,-s, s)
    glTexCoord2f(1,0); glVertex3f( s,-s, s)
    glTexCoord2f(1,1); glVertex3f( s, s, s)
    glTexCoord2f(0,1); glVertex3f(-s, s, s)
    # trás
    glNormal3f(0,0,-1)
    glTexCoord2f(0,0); glVertex3f( s,-s,-s)
    glTexCoord2f(1,0); glVertex3f(-s,-s,-s)
    glTexCoord2f(1,1); glVertex3f(-s, s,-s)
    glTexCoord2f(0,1); glVertex3f( s, s,-s)
    # esquerda
    glNormal3f(-1,0,0)
    glTexCoord2f(0,0); glVertex3f(-s,-s,-s)
    glTexCoord2f(1,0); glVertex3f(-s,-s, s)
    glTexCoord2f(1,1); glVertex3f(-s, s, s)
    glTexCoord2f(0,1); glVertex3f(-s, s,-s)
    # direita
    glNormal3f(1,0,0)
    glTexCoord2f(0,0); glVertex3f( s,-s, s)
    glTexCoord2f(1,0); glVertex3f( s,-s,-s)
    glTexCoord2f(1,1); glVertex3f( s, s,-s)
    glTexCoord2f(0,1); glVertex3f( s, s, s)
    # topo
    glNormal3f(0,1,0)
    glTexCoord2f(0,0); glVertex3f(-s, s, s)
    glTexCoord2f(1,0); glVertex3f( s, s, s)
    glTexCoord2f(1,1); glVertex3f( s, s,-s)
    glTexCoord2f(0,1); glVertex3f(-s, s,-s)
    # base
    glNormal3f(0,-1,0)
    glTexCoord2f(0,0); glVertex3f(-s,-s,-s)
    glTexCoord2f(1,0); glVertex3f( s,-s,-s)
    glTexCoord2f(1,1); glVertex3f( s,-s, s)
    glTexCoord2f(0,1); glVertex3f(-s,-s, s)
    glEnd()

def main():
    global angle, use_linear
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Texturas: Carga + Mip-Mapping (toggle filtro: F)")
    init()
    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type==QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                running=False
            if e.type==KEYDOWN and e.key==K_f:
                use_linear = not use_linear
                glBindTexture(GL_TEXTURE_2D, tex_id)
                set_filters()

        angle += 0.8
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,1.8,7, 0,0,0, 0,1,0)

        glRotatef(angle, 1,1,0)
        textured_cube()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
