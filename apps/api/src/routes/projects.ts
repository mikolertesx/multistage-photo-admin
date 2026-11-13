import type { LambdaEvent, LambdaContext } from '@hono/aws-lambda';
import {Hono} from 'hono';

type Bindings = {
    event: LambdaEvent
    lambdaContext: LambdaContext
  }

const app = new Hono<{Bindings: Bindings}>();

app.get('/create-project', (c) => {

    const project_name = c.req.query('project_name');
    return  c.json({
        message: `Create project ${project_name}`,
        env: c.req.queries(),
    });
});


app.get('/get-project-list', (c) => {
    return c.json({
        message: 'Get project list',
    });
});

export default app;
