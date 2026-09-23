import { useEffect } from 'react'
import { GetObjectCommand, S3Client } from '@aws-sdk/client-s3'
import { appEnv, siteName } from './env'

const s3 = new S3Client({
  region: 'us-east-1',
  requestChecksumCalculation: 'WHEN_REQUIRED',
  responseChecksumValidation: 'WHEN_REQUIRED',
  httpAuthSchemeProvider: () => [{ schemeId: 'smithy.api#noAuth' }],
  httpAuthSchemes: [
    {
      schemeId: 'smithy.api#noAuth',
      identityProvider: () => async () => ({}),
      signer: { sign: async (request) => request },
    },
  ],
})

function App() {
  useEffect(() => {
    s3
      .send(
        new GetObjectCommand({
          Bucket: 'multistage-photo-admin-media-bucket',
          Key: 'hello.txt',
        }),
      )
      .then((output) => output.Body?.transformToString())
      .then((text) => {
        console.log(text)
      })
      .catch((error: unknown) => {
        console.log(error)
      })
  }, [])

  return (
    <main className="page">
      <p className="env">{appEnv}</p>
      <h1>{siteName}</h1>
      <p>React app deployed with Terraform to S3 and CloudFront.</p>
    </main>
  )
}

export default App
