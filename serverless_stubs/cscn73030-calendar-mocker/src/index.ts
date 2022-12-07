import { Router } from '@tsndr/cloudflare-worker-router'
import { CALENDAR_EVENTS } from './event_data'

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


/* 
This code stubs the Calendar service.

NOT IMPLEMENTED: GET /events?startRange=[datetime]&endRange=[datetime]

There is minimal testing on posting and deletion
*/

// Helpers
const TAG_CHOICES: Array<string> = ["quiz", "survey", "assignment"]


class RandomEvent {
	eID: string = "ERROR"
	title: string = "ERROR"
	startDate: string = "ERROR"
	endDate: string = "ERROR"
	tag: string = "ERROR"
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
	if ("enterpriseID" in req.query) {
		res.body = { "eID": "c 27", "title": "Event Title 16", "startDate": "2022-11-04T15:05:23", "endDate": "2022-11-18T15:23:21", "tag": "quiz" }
		res.body.eID = req.query["enterpriseID"]
	}
	else {
		res.body = { "eID": "c 24", "title": "Event Title 71", "startDate": "2022-11-22T15:21:14", "endDate": "2022-11-14T20:37:32", "tag": "survey" }
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

router.get("/events", ({ req, res }) => {
	if ("eventType" in req.query) {
		let req_tag = req.query["eventType"]
		console.log("Requested event of type: " + req_tag)

		if (TAG_CHOICES.includes(req_tag)) {
			let result = CALENDAR_EVENTS.filter(({ tag }) => tag == req_tag)
			res.body = result
		}
		else {
			res.body = "Invalid type, pick one of " + TAG_CHOICES.toString()
			res.status = 404
		}

	} else if ("amount" in req.query) {

		let req_amt = parseInt(req.query["amount"])
		console.log("Requested " + req_amt.toString() + " events")

		if (isNaN(req_amt)) {
			res.status = 400
			res.body = "Please specify a numeric amount"
		}
		else {
			res.body = CALENDAR_EVENTS.slice(0, req_amt)
		}

	} else {
		res.body = CALENDAR_EVENTS
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