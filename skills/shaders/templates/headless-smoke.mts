import { readFileSync, writeFileSync } from "node:fs";
import { effect, init, target } from "vgpu/node";

const size = 64;

async function main() {
  const source = readFileSync(new URL("./static-field.wgsl", import.meta.url), "utf8");
  const gpu = await init({ adapter: "software" });
  try {
    const output = target(gpu, { size: [size, size], format: "rgba8unorm" });
    effect(gpu, source).draw(output);
    writeFileSync("static-field.rgba", await output.read());
    await gpu.settled();
  } finally {
    gpu.dispose();
  }
}

void main();
