#[no_mangle]
pub fn rgb_to_ycocg(r: u8, g: u8, b: u8) -> (u8, i8, i8) {
	let y = r / 4 + g / 2 + b / 4;
	let co = (r / 2 - b / 2) as i8;
	let cg = -((r / 4) as i8) + (g / 2) as i8 + -((b / 4) as i8);
	(y, co, cg)
}

#[no_mangle]
pub fn ycocg_to_rgb(y: u8, co: i8, cg: i8) -> (u8, u8, u8) {
	let r = y.wrapping_add_signed(co.wrapping_sub(cg));
	let g = y.wrapping_add_signed(cg);
	let b = (y as i8).wrapping_sub(co).wrapping_sub(cg) as u8;
	(r, g, b)
}

#[cfg(test)]
mod test {
	use crate::ycocg::*;

	#[test]
	fn test_ycocg_royal_red() {
		let (y, co, cg) = rgb_to_ycocg(255, 128, 64);
		assert_eq!((y, co, cg), (143, 95, -15));
		let (r, g, b) = ycocg_to_rgb(y, co, cg);
		assert_eq!((r, g, b), (253, 128, 63));
	}

	#[test]
	fn test_ycocg_white() {
		let (y, co, cg) = rgb_to_ycocg(255, 255, 255);
		assert_eq!((y, co, cg), (253, 0, 1));
		let (r, g, b) = ycocg_to_rgb(y, co, cg);
		assert_eq!((r, g, b), (252, 254, 252));
	}
}
