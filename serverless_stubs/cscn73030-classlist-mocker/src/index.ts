import { Router } from '@tsndr/cloudflare-worker-router'
import { CLASSLIST } from './data';


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


class Student {
	firstname: string = "ERROR"
	lastname: string = "ERROR"
	email: string = "ERROR"
	studentNumber: number = -1
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
	res.body = CLASSLIST
})

// TODO: Figure out what the exact format of this is
router.get("/students/classSize", ({ req, res }) => {
	res.body = CLASSLIST.length
})

router.get("/students/:id", ({ req, res }) => {
	let search_id = parseInt(req.params.id)

	if (isNaN(search_id)) {
		res.status = 400
		res.body = "Please enter a numerical ID"
	}
	else {
		console.log("Looking for ID ", search_id)

		let filtered = CLASSLIST.filter(
			student => student.studentNumber == search_id
		)

		console.log("Found: ", filtered)

		if (filtered.length == 1) {
			res.body = filtered[0]
			res.status = 200
		} else {
			res.body = "NOT FOUND"
			res.status = 404
		}
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