# Geometry and Scenes

## When to use

Use for custom vertex/fragment draws, meshes, cameras, transformations, normals, lighting, materials, depth, instancing, and vgpu scene helpers.

## Inputs

- geometry topology, attributes, index format, bounds, and coordinate convention;
- camera/projection, transform hierarchy, lighting, material, and transparency requirements;
- depth/MSAA/target formats and render ordering;
- interaction, resize, performance, and asset-loading constraints.

## Procedure

1. Decide whether `vgpu/scene` expresses the task or a custom `draw` is necessary.
2. Read installed docs for draws, geometry, camera/material helpers, and two-pass depth before implementing.
3. Render one unlit object in a deterministic pose and solid color.
4. Verify transform landmarks and winding/culling before adding lighting.
5. Display normals as RGB, then add one light and one material term at a time.
6. Add depth through an offscreen target when the scene requires it; canvas surfaces do not imply the depth attachment needed by real 3D geometry.
7. Add camera controls only after static camera math passes.
8. Move repeated geometry to instancing or shared buffers before scaling object count.
9. Measure representative scene complexity, not the one-object proof.

## Transform rules

- Declare matrix order and vector convention once.
- Keep model, world, view, projection, and normal transforms distinct.
- Transform normals with the inverse transpose when nonuniform scale exists.
- Normalize directions after interpolation and non-orthonormal transforms.
- Preserve stable parent-child ownership; avoid recomputing unchanged world matrices each frame.
- Test identity, translation, axis rotations, uniform/nonuniform scale, and nested transforms.

## Geometry rules

- Validate attribute layouts, strides, offsets, formats, and index range against reflection.
- Keep winding and culling consistent; use a diagnostic two-sided mode only to locate errors.
- Compute bounds and inspect them before camera fitting or culling.
- Recompute or transform normals deliberately after mesh edits.
- Use wireframe, normal, and readable-mesh inspection helpers for topology bugs.
- Avoid duplicated vertices unless UV seams, normals, materials, or topology require them.

## Lighting and materials

- Start with linear-space diffuse lighting and a controlled exposure.
- Separate geometric normal, shading normal, view direction, light direction, and half vector.
- Clamp dot products before powers; guard zero-length directions.
- Preserve energy intentionally when combining diffuse, specular, transmission, and emission.
- Tone-map at the output boundary and verify colors in the actual canvas format.
- Debug materials with flat color, UV, normals, depth, roughness, and light contribution views.

## Depth, transparency, and ordering

- Choose depth format and clear value from the projection convention.
- Use depth write/test settings that match opaque, cutout, or transparent material behavior.
- Alpha blending is order-dependent; sort or use an appropriate technique rather than assuming arbitrary transparency works.
- Match straight/premultiplied shader output to blend factors.
- Inspect coplanar surfaces, near/far precision, intersections, and transparent silhouettes.

## Camera and interaction

- Keep projection aspect in sync with physical target size.
- Bound orbit/zoom controls and define pole behavior.
- Map pointer coordinates from client pixels to canvas physical pixels correctly.
- Clean up control listeners and stop updates when the scene is disposed.
- Provide keyboard/touch-equivalent interaction when camera movement is necessary to access content.

## Completion

Transforms, winding, bounds, normals, depth, and material terms pass diagnostic views; the scene renders deterministically in Node, behaves correctly in the browser across resize/input, disposes cleanly, and meets the representative object-count budget.

## Escalate

Escalate unsupported asset formats, ambiguous handedness/projection inherited from external data, transparency requirements needing a new rendering technique, or scene complexity beyond the chosen device budget.
