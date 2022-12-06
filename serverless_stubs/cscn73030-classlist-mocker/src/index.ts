import { Router } from '@tsndr/cloudflare-worker-router'
import { uniqueNamesGenerator, Config, colors, animals } from 'unique-names-generator';


export interface Env {
	// Example binding to KV. Learn more at https://developers.cloudflare.com/workers/runtime-apis/kv/
	// MY_KV_NAMESPACE: KVNamespace
	//
	// Example binding to Durable Object. Learn more at https://developers.cloudflare.com/workers/runtime-apis/durable-objects/
	// MY_DURABLE_OBJECT: DurableObjectNamespace
	//
	// Example binding to R2. Learn more at https://developers.cloudflare.com/workers/runtime-apis/r2/
	// MY_BUCKET: R2Bucket
}

// Helpers

// Returns a number between 0 and `max` (default=100)
function getRandomNumber(max: number = 100): number {
	return Math.floor(Math.random() * max)
}


class Student {
	firstname: string
	lastname: string
	email: string
	studentNumber: number

	constructor() {
		this.firstname = uniqueNamesGenerator({ dictionaries: [colors] })
		this.lastname = uniqueNamesGenerator({ dictionaries: [animals] })
		this.email = this.firstname + "." + this.lastname + getRandomNumber() + "@example.com"
		this.studentNumber = getRandomNumber(20000000)
	}
}



// Initialize router
const router = new Router<Env>()

// Enabling build in CORS support
router.cors()

// Register global middleware
router.use(({ req, res, next }) => {
	res.headers.set('X-Global-Middlewares', 'true')
	next()
})

// Return random number of students
router.get('/students', ({ req, res }) => {
	let return_number = getRandomNumber()

	res.body = new Array(return_number).fill("").map((_, i) => new Student)
})

// TODO: Figure out what the exact format of this is
router.get("/students/classSize", ({ req, res }) => {
	res.body = getRandomNumber()
})

router.get("/students/:id", ({ req, res }) => {
	const student_id = parseInt(req.params.id)

	if (isNaN(student_id)) {
		res.status = 400
		res.body = "Please enter a numerical ID"
	}
	else {
		let result = new Student
		result.studentNumber = student_id
		res.body = result
	}
})


router.post("/students", ({ req, res }) => {
	let creation: Student = JSON.parse(req.body)

	res.status = 201
})


router.delete("/students/:id", ({ req, res }) => {
	const student_id = parseInt(req.params.id)

	if (isNaN(student_id)) {
		res.status = 400
		res.body = "Please enter a numerical ID"
	}
	else {
		res.status = 202
	}
})

router.put("/students", ({ req, res }) => {
	let creation: Student = JSON.parse(req.body)

	res.status = 201
})


// Listen Cloudflare Workers Fetch Event
export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		return router.handle(env, request)
	}
}