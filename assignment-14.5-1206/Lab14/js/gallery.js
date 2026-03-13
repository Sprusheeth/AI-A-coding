const modal = document.getElementById('galleryModal');
const modalImage = document.getElementById('modalImage');
const closeButton = document.getElementById('closeModal');
const thumbButtons = document.querySelectorAll('[data-full]');

function openModal(src, altText) {
  modalImage.src = src;
  modalImage.alt = altText || 'Gallery preview';
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
}

function closeModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
}

thumbButtons.forEach((button) => {
  button.addEventListener('click', () => {
    openModal(button.dataset.full, button.dataset.alt);
  });
});

closeButton.addEventListener('click', closeModal);

modal.addEventListener('click', (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && modal.classList.contains('open')) {
    closeModal();
  }
});
