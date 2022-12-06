import { Router } from '@tsndr/cloudflare-worker-router'

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



// Initialize router
const router = new Router<Env>()

// Enabling build in CORS support
router.cors()

// Register global middleware
router.use(({ req, res, next }) => {
	res.headers.set('X-Global-Middlewares', 'true')
	next()
})

// return mode of operation
router.get('/modeofoperation', ({ req, res }) => {
	res.body = {
		"modeofoperation": false
	}
})


router.post("/togglemode", ({ req, res }) => {
	res.status = 200
})

router.post("/announcement", ({ req, res }) => {
	res.status = 201
})

router.put("/announcement", ({ req, res }) => {
	if ("id" in req.query) {
		let id = parseInt(req.query["id"])

		if (isNaN(id)) {
			res.body = "Please supply a numerical ID"
			res.status = 400
		}
		else {
			res.status = 201
		}
	}
	else {
		res.body = "Please supply a numerical ID"
		res.status = 400
	}
})

router.delete("/announcement", ({ req, res }) => {
	if ("id" in req.query) {
		let id = parseInt(req.query["id"])

		if (isNaN(id)) {
			res.body = "Please supply a numerical ID"
			res.status = 400
		}
		else {
			res.status = 201
		}
	}
	else {
		res.body = "Please supply a numerical ID"
		res.status = 400
	}
})


// Listen Cloudflare Workers Fetch Event
export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		return router.handle(env, request)
	}
}