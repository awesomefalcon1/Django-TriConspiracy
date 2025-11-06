import Events from '@/components/Events';
import Projects from '@/components/Projects';

export default function Home() {
  return (
    <main className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <section className="mb-12">
          <h1 className="text-4xl font-bold mb-4">Welcome to DKK</h1>
          <p className="text-gray-400 text-lg">
            Discover our projects and upcoming events
          </p>
        </section>

        <div className="space-y-12">
          <Projects />
          <Events />
        </div>
      </div>
    </main>
  );
}
