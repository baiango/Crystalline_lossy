use crystalline_lossy::ycocg;


fn main() {
	println!("Hello, world!");
	let (y, co, cg) = ycocg::rgb_to_ycocg(255, 255, 255);
	println!("Y: {}, Co: {}, Cg: {}", y, co, cg);
}
