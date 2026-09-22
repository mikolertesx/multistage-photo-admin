import { appEnv, siteName } from './env'

function App() {
  return (
    <main className="page">
      <p className="env">{appEnv}</p>
      <h1>{siteName}</h1>
      <p>React app deployed with Terraform to S3 and CloudFront.</p>
    </main>
  )
}

export default App
