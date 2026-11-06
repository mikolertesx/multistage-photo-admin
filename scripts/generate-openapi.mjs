import {execFileSync, spawn} from 'node:child_process'
import {fileURLToPath} from 'node:url'
import { writeFileSync } from 'node:fs'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

const raw = execFileSync(
    'terraform',
    ['-chdir=infra', 'output', '-json'],
    { cwd: root, encoding: 'utf-8'}
)

const outputs = JSON.parse(raw)
const openapiBody = outputs.openapi?.value

if (typeof openapiBody !== 'string' || openapiBody === '') {
    console.error('Terraform output openAPI is missing. Apply infra first.')
    process.exit(1)
} 

writeFileSync(path.resolve(root, 'api', 'swagger.json'), openapiBody)

execFileSync(
    'pnpm',
    ['exec', 'openapi-ts', '-i', './api/swagger.json', '-o', 'apps/web/src/api', '-c', '@hey-api/client-axios']
)
