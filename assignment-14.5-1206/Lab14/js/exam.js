const questions = [
  {
    question: 'Which HTML element is used for the largest heading?',
    options: ['<h6>', '<heading>', '<h1>', '<head>'],
    answer: 2
  },
  {
    question: 'Which CSS layout is best suited for two-dimensional page areas?',
    options: ['Float', 'Flexbox', 'Grid', 'Inline-block'],
    answer: 2
  },
  {
    question: 'Which keyword declares a block-scoped variable in JavaScript?',
    options: ['var', 'let', 'const', 'both let and const'],
    answer: 3
  },
  {
    question: 'What does localStorage primarily store?',
    options: ['Binary files only', 'Key-value strings in browser', 'Server logs', 'Cookies only'],
    answer: 1
  },
  {
    question: 'Which attribute improves accessibility for form inputs?',
    options: ['style', 'onclick', 'aria-label', 'width'],
    answer: 2
  }
];

const EXAM_KEY = 'lab14_exam_submitted';
let currentIndex = 0;
let remaining = 180;
let submitted = localStorage.getItem(EXAM_KEY) === 'true';
const answers = {};
let timerId;

const timerEl = document.getElementById('timer');
const questionCountEl = document.getElementById('questionCount');
const questionTextEl = document.getElementById('questionText');
const optionsEl = document.getElementById('options');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const resultEl = document.getElementById('result');

function formatTime(seconds) {
  const mins = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  return `${mins}:${secs}`;
}

function renderQuestion() {
  const q = questions[currentIndex];
  questionCountEl.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
  questionTextEl.textContent = q.question;

  optionsEl.innerHTML = q.options
    .map(
      (option, idx) => `
      <label>
        <input type="radio" name="option" value="${idx}" ${answers[currentIndex] === idx ? 'checked' : ''} ${submitted ? 'disabled' : ''}>
        <span>${option}</span>
      </label>
    `
    )
    .join('');

  optionsEl.querySelectorAll('input[type="radio"]').forEach((input) => {
    input.addEventListener('change', () => {
      answers[currentIndex] = Number(input.value);
    });
  });

  prevBtn.disabled = currentIndex === 0 || submitted;
  nextBtn.disabled = currentIndex === questions.length - 1 || submitted;
}

function submitExam(auto = false) {
  if (submitted) {
    return;
  }

  submitted = true;
  localStorage.setItem(EXAM_KEY, 'true');
  clearInterval(timerId);

  let score = 0;
  questions.forEach((q, index) => {
    if (answers[index] === q.answer) {
      score += 1;
    }
  });

  resultEl.textContent = auto
    ? `Time is up. Your score is ${score} / ${questions.length}.`
    : `Exam submitted. Your score is ${score} / ${questions.length}.`;

  submitBtn.disabled = true;
  prevBtn.disabled = true;
  nextBtn.disabled = true;
  renderQuestion();
}

function tick() {
  timerEl.textContent = formatTime(remaining);
  if (remaining <= 0) {
    submitExam(true);
    return;
  }
  remaining -= 1;
}

prevBtn.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex -= 1;
    renderQuestion();
  }
});

nextBtn.addEventListener('click', () => {
  if (currentIndex < questions.length - 1) {
    currentIndex += 1;
    renderQuestion();
  }
});

submitBtn.addEventListener('click', () => submitExam(false));

document.getElementById('resetExam').addEventListener('click', () => {
  localStorage.removeItem(EXAM_KEY);
  window.location.reload();
});

if (submitted) {
  resultEl.textContent = 'This exam was already submitted on this browser. Click Reset Exam to try again.';
  submitBtn.disabled = true;
  prevBtn.disabled = true;
  nextBtn.disabled = true;
  timerEl.textContent = '00:00';
  renderQuestion();
} else {
  timerId = setInterval(tick, 1000);
  tick();
  renderQuestion();
}
