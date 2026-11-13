import { Hono } from 'hono'

import projects from './routes/projects';

const app = new Hono()

app.get('/', (c) => c.json({ ok: true }))
app.route('/projects', projects);

export type AppType = typeof app

export { app }
