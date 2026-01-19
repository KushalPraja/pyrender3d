goal

- implement a 3d cube render in pygame using projection
- we have to implement the Tait-Bryan angles for camera rotation

- https://en.wikipedia.org/wiki/3D_projection

-- implement better mouse movement
-- implement better rendering scheme
-- implement character collisions

- current issues:

FPS is very low
-- I think this is happening because our program is not utilizing the GPU at all and thus
it is not optimizing the triangle loading. It would be useful down the line to implement pyOPENGL but I
am not to familiar with it so thats that
