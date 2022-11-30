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
const TAG_CHOICES: Array<string> = ["quiz", "survey", "assignment"]

// Returns a number between 0 and `max` (default=100)
function getRandomNumber(max: number = 100): number {
	return Math.floor(Math.random() * max)
}

function getPaddedNumberString(max: number = 59, padding: number = 2): string {
	let value = getRandomNumber(max).toString()

	return value.padStart(padding, "000")
}

function getRandomDate() {
	let year: string = "2022"
	let month: string = "11"
	let day: string = getPaddedNumberString(30)
	let hour: string = getPaddedNumberString(23)
	let minute: string = getPaddedNumberString(59)
	let second: string = getPaddedNumberString(59)


	return `${year}-${month}-${day}T${hour}:${minute}:${second}`
}

function getRandomTag() {

	let my_choice: number = getRandomNumber(2)

	return TAG_CHOICES[my_choice]
}


class RandomEvent {
	eID: string
	title: string
	startDate: string
	endDate: string
	tag: string

	constructor() {
		this.eID = "c " + getRandomNumber();
		this.title = "Event Title " + getRandomNumber()
		this.startDate = getRandomDate()
		this.endDate = getRandomDate()
		this.tag = getRandomTag()
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

// Gets
router.get('/event', ({ req, res }) => {
	// Generate amount of objects
	if ("amount" in req.query) {
		let req_amt = parseInt(req.query["amount"])
		console.log("Requested " + req_amt.toString() + " events")

		if (isNaN(req_amt)) {
			res.status = 400
			res.body = "Please specify a numeric amount"
		}
		else {
			res.body = new Array(req_amt).fill("").map((_, i) => new RandomEvent)
		}


	}
	else if ("eventType" in req.query) {
		let req_tag = req.query["eventType"]
		console.log("Requested event of type: " + req_tag)

		if (TAG_CHOICES.includes(req_tag)) {
			let result = new RandomEvent

			while (!(TAG_CHOICES.includes(result.tag))) {
				result = new RandomEvent
			}

			res.body = result
		}
		else {
			res.body = "Invalid type, pick one of " + TAG_CHOICES.toString()
			res.status = 404
		}
	}
	else if ("enterpriseID" in req.query) {
		res.body = new RandomEvent
		res.body.eID = req.query["enterpriseID"]
	}
	else {
		res.body = new RandomEvent
	}
})

router.post("/event", ({ req, res }) => {
	let creation: RandomEvent = JSON.parse(req.body)

	res.status = 201
})

router.put("/event", ({ req, res }) => {
	if ("enterpriseID" in req.query) {
		res.status = 200
	}
	else {
		res.status = 400
		res.body = "Require enterpriseID query string"
	}
})

router.delete("/event", ({ req, res }) => {
	if ("enterpriseID" in req.query) {
		res.status = 200
	}
	else {
		res.status = 400
		res.body = "Require enterpriseID query string"
	}
})

// Listen Cloudflare Workers Fetch Event
export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		return router.handle(env, request)
	}
}