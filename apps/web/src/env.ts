export type AppEnv = 'dev' | 'staging' | 'prod'

const raw = (import.meta.env.VITE_APP_ENV ?? 'dev').toLowerCase()

export const appEnv: AppEnv =
  raw === 'staging' || raw === 'prod' || raw === 'dev' ? raw : 'dev'

export const siteName = import.meta.env.VITE_SITE_NAME ?? 'Multistage Admin'
