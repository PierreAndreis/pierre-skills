@fragment
fn fs_main(@location(0) uv: vec2f) -> @location(0) vec4f {
  let centered = uv * 2.0 - 1.0;
  let radius = length(centered);
  let edge = 1.0 - smoothstep(0.2, 0.9, radius);
  let cool = vec3f(0.08, 0.16, 0.34);
  let warm = vec3f(0.94, 0.45, 0.18);
  return vec4f(mix(cool, warm, edge), 1.0);
}
