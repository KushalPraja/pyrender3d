# PyRender3d

This goal of this project was to implement a very simple 3d rendering engine using projections and pygame.

### Implementation Notes

This projects just uses simple projections for rendering and not any 3d libraries. This results in the load going to the cpu and lack of multi-threading, resulting in low frames (20-30 fps tested on intel i7 14650hx). 
However to optimize, I implemented backface culling, and low render distances to improve the fps slightly. 

### resources:

- https://en.wikipedia.org/wiki/3D_projection
- https://songho.ca/opengl/gl_camera.html
- https://gamemath.com/book/

**Images**

_Wireframe Mode:_
<img width="1920" height="1080" alt="Screenshot 2026-01-20 183436" src="https://github.com/user-attachments/assets/82f27056-26c8-49d6-85c9-4847960b7aeb" />

_Post-Rasterization:_
<img width="1920" height="1080" alt="Screenshot 2026-01-20 183502" src="https://github.com/user-attachments/assets/ef02e9c5-ae0e-4227-a36f-3c206413b443" />
