import React from 'react';
import Image from 'next/image';
import eventsData from '@/app/data/events.json';

interface Event {
  name: string;
  date: string;
  description: string;
  image: string;
  location: string;
  registrationLink: string;
}

function Events() {
  return (
    <section>
      <h2 className="text-3xl font-bold mb-6">WIP: Upcoming Events</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {eventsData.map((event: Event, index: number) => (
          <div key={index} className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
            <div className="relative w-full h-48">
              <Image 
                src={event.image} 
                alt={event.name} 
                fill
                style={{ objectFit: 'cover' }}
              />
            </div>
            <div className="p-4">
              <h3 className="text-xl font-bold mb-2">{event.name}</h3>
              <p className="text-gray-400 mb-2">{event.date}</p>
              <p className="text-gray-400">{event.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Events;
