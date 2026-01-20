# PyRender3d

This goal of this project was to implement a 3d rendering engine
using pygame.

### Why pygame?

I don't currently know enough about C++ and OPENGL to implement these same algorithms.
I also feel more comfortable with python classes and OOP right now. Even though I just learned pygame, I found the syntax to be quite easy and the documentation is really good.

_Most Importantly_, I'm still learning graphics programming and the main goal was to learn the algorithms rather than optimize. The idea of different spaces(world space, camera space, screen space) was quite new to me and I hadn't ever played around with projections before.

This project has allowed me to experiment and learn about **projections, transformations, rendering pipelines using matrices and numpy**.
Even though this code is quite rough, I think I'm excited to create similar projects as I found this one to be really enjoyable and I have even more ideas for creating games using these algos.

I think for the future, I will try to use OPENGL and CUDA to implement these same algorithms and compare the FPS.

**I will attach notes to this readme after I am done with the project**

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
