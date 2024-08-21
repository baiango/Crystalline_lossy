pub fn rgb_to_ycocg(r: u8, g: u8, b: u8) -> (u8, i8, i8) {
	let y = r / 4 + g / 2 + b / 4;
	let co = (r as i16 - b as i16) / 2;
	let cg = -(r as i16 / 4) + g as i16 / 2 + -(b as i16 / 4);
	(y, co as i8, cg as i8)
}

pub fn ycocg_to_rgb(y: u8, co: i8, cg: i8) -> (u8, u8, u8) {
	let y = y as i16;
	let co = co as i16;
	let cg = cg as i16;
	let r = y + co - cg;
	let g = y + cg;
	let b = y - co - cg;
	(r as u8, g as u8, b as u8)
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

	#[test]
	fn test_ycocg_yellow() {
		let (y, co, cg) = rgb_to_ycocg(255, 255, 0);
		assert_eq!((y, co, cg), (190, 127, 64));
		let (r, g, b) = ycocg_to_rgb(y, co, cg);
		assert_eq!((r, g, b), (253, 254, 255));
	}

	#[test]
	fn test_ycocg_aqua() {
		let (y, co, cg) = rgb_to_ycocg(0, 255, 255);
		assert_eq!((y, co, cg), (190, -127, 64));
		let (r, g, b) = ycocg_to_rgb(y, co, cg);
		assert_eq!((r, g, b), (255, 254, 253));
	}
}
