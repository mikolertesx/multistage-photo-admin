import {execFileSync, spawn} from 'node:child_process'
import {fileURLToPath} from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const task = process.argv[2]

const raw = execFileSync(
    'terraform',
    ['-chdir=infra', 'output', '-json'],
    { cwd: root, encoding: 'utf-8'}
)

const outputs = JSON.parse(raw)
const apiUrl = outputs.apigateway_url?.value

if (typeof apiUrl !== 'string' || apiUrl === '') {
    console.error('Terraform ouptut apigateway_url is missing. Apply infra first.')
    process.exit(1)
} 

const child = spawn('pnpm', ['--filter', 'web', task], {
    cwd: root,
    stdio: 'inherit',
    env: {...process.env, VITE_API_URL: apiUrl},
})

child.on('exit', (code) => process.exit(code ?? 1))

