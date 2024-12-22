import os

# Define the project structure
project_structure = {
    "matrix-devops-automation": {
        "public": {
            "assets": {}  # Placeholder for static assets like images/icons
        },
        "styles": {
            "globals.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-black text-green-500;
}
"""
        },
        "pages": {
            "index.js": """
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-green-500 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-8">Welcome to the Matrix of DevOps</h1>
      <p className="text-lg mb-4">Are you into:</p>
      <div className="flex gap-6">
        <Link href="/choose-pill?role=product-development">
          <a className="bg-green-700 px-6 py-3 rounded-lg hover:bg-green-800 transition">Product Development</a>
        </Link>
        <Link href="/choose-pill?role=client-services">
          <a className="bg-green-700 px-6 py-3 rounded-lg hover:bg-green-800 transition">Helping Clients</a>
        </Link>
      </div>
    </div>
  );
}
""",
            "choose-pill.js": """
import Link from 'next/link';

export default function ChoosePill() {
  return (
    <div className="min-h-screen bg-black text-green-500 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-6">Choose Your Path</h1>
      <p className="text-lg mb-4">Are you ready to explore reality or stay in the illusion?</p>
      <div className="flex gap-6">
        <Link href="/red-pill">
          <a className="bg-red-700 px-6 py-3 rounded-lg hover:bg-red-800 transition">Red Pill</a>
        </Link>
        <Link href="/blue-pill">
          <a className="bg-blue-700 px-6 py-3 rounded-lg hover:bg-blue-800 transition">Blue Pill</a>
        </Link>
      </div>
    </div>
  );
}
""",
            "red-pill.js": """
export default function RedPill() {
  const aspects = [
    { aspect: 'Automation Scope', value: 'End-to-end CI/CD pipelines covering all stages.' },
  ];

  return (
    <div className="min-h-screen bg-black text-green-500 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">The Harsh Reality: Red Pill</h1>
      <div className="w-full max-w-4xl bg-gray-900 p-6 rounded-lg shadow-lg">
        <table className="table-auto w-full text-left text-green-500">
          <thead>
            <tr className="border-b border-green-700">
              <th className="px-4 py-2 text-lg">Aspect</th>
              <th className="px-4 py-2 text-lg">Reality (Red Pill)</th>
            </tr>
          </thead>
          <tbody>
            {aspects.map((item, index) => (
              <tr key={index} className="border-b border-green-700">
                <td className="px-4 py-2 font-semibold">{item.aspect}</td>
                <td className="px-4 py-2">{item.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
""",
            "blue-pill.js": """
export default function BluePill() {
  const aspects = [
    { aspect: 'Automation Scope', value: 'Basic task automation (e.g., Jenkins jobs).' },
  ];

  return (
    <div className="min-h-screen bg-black text-green-500 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">The Comfortable Illusion: Blue Pill</h1>
      <div className="w-full max-w-4xl bg-gray-900 p-6 rounded-lg shadow-lg">
        <table className="table-auto w-full text-left text-green-500">
          <thead>
            <tr className="border-b border-green-700">
              <th className="px-4 py-2 text-lg">Aspect</th>
              <th className="px-4 py-2 text-lg">Illusion (Blue Pill)</th>
            </tr>
          </thead>
          <tbody>
            {aspects.map((item, index) => (
              <tr key={index} className="border-b border-green-700">
                <td className="px-4 py-2 font-semibold">{item.aspect}</td>
                <td className="px-4 py-2">{item.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
        },
        "components": {
            "Layout.js": """
export default function Layout({ children }) {
  return <div className="container mx-auto p-4">{children}</div>;
}
""",
            "Header.js": """
export default function Header() {
  return (
    <header className="absolute top-4 right-4 text-green-500">
      <button className="bg-green-700 px-4 py-2 rounded hover:bg-green-800">
        Toggle Accessibility
      </button>
    </header>
  );
}
"""
        },
        "tailwind.config.js": """
module.exports = {
  content: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        black: '#000000',
        green: {
          500: '#00FF00',
          700: '#008000',
          800: '#006400',
        },
      },
    },
  },
};
""",
        "package.json": """
{
  "name": "matrix-devops-automation",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "latest",
    "react": "latest",
    "react-dom": "latest",
    "tailwindcss": "latest"
  }
}
""",
        "next.config.js": """
module.exports = {
  reactStrictMode: true,
};
"""
    }
}

# Function to create the directory structure and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as file:
                file.write(content)

# Execute script
base_directory = "./"
create_structure(base_directory, project_structure)
print("Project structure created successfully!")
