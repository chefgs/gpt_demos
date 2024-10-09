// prisma/seed.js
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  await prisma.quiz.create({
    data: {
      question: 'What is the capital of France?',
      answers: ['Paris', 'London', 'Berlin', 'Madrid'],
      correctAnswer: 'Paris',
      category: 'Geography',
      difficulty: 'Easy',
    },
  });

  const allQuizzes = await prisma.quiz.findMany();
  console.log(allQuizzes);
}

main()
  .catch((e) => {
    throw e;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });