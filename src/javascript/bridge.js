const Bridge = require("@molfar/py-bridge")
const path = require("path")

const DepParse = class extends Bridge {
	constructor(config){
		super(config)
		this.use("__run",path.resolve(__dirname,"../python/depparse.py"))
	}

	getDepParse(text) {
		return this.__run({
			method: "extract_dependencies",
			params: { text }
		})
	}
}

module.exports = DepParse

// const run = async () => {
//
// 	const config = {
// 		mode: 'text',
// 		encoding: 'utf8',
// 		pythonOptions: ['-u'],
// 		pythonPath: (process.env.NODE_ENV && process.env.NODE_ENV === "production") ? "python" : "python.exe",
// 		args: `en ${path.resolve(__dirname, "./Stanza-models")}`
// 	}
//
// 	const extractor = new DepParse(config)
// 	extractor.start()
//
// 	const text = `United States of America is a country. Barack Obama was a president of it. His daughters are Sasha and Malia.`
// 	console.log(text)
// 	let res = await extractor.getDepParse(text)
//
// 	console.log(res)
// 	extractor.terminate()
// }
//
// run()
