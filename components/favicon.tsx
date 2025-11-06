import Head from 'next/head'

export default function Favicon() {
  return (
    <Head>
      <link rel="icon" href="/favicon.ico" sizes="any" />
      <link rel="apple-touch-icon" href="/favicon.ico" />
    </Head>
  )
}

