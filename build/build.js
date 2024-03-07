const { extend } = require("lodash")
const chalk = require("chalk")
const fse = require("fs-extra")
const path = require("path")
const execa = require("execa")

const config = extend(require(path.resolve(__dirname, "../package.json")).depparse, require("./build.config"))
console.log("MOLFAR DEPPARSE SERVICE POSTINSTALL")

console.log(`Creating model directory ${config.models.destDir}...`)
fse.mkdirs(config.models.destDir).then((result) => {
		console.log(chalk.green(`Created model directory ${config.models.destDir}`))
		return result
	})

	.then(() => {
		console.log("Installing Python packages...")
		const installer = execa("pip", "install -r requirements.txt".split(" "))
		const stream = installer.stdout
		stream.pipe(process.stdout)
		return installer
	}).then((result) => {
		console.log(chalk.green("Installed Python packages"))
		return result
	})

	.then(() => {
		console.log(`Downloading Stanza model for '${config.service.lang}' language into ${config.models.destDir}...`)
		const installer = execa("python", [
			path.resolve(__dirname, "./download.py"),
			config.service.lang,
			config.models.destDir,
		])
		const stream = installer.stdout
		stream.pipe(process.stdout)
		return installer
	}).then((result) => {
		console.log(chalk.green(`Downloaded Stanza model for '${config.service.lang}' language into ${config.models.destDir}`))
		return result
	})

	.catch( e => {
		console.error(chalk.red(e.toString()))
	})
