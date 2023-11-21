  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      var classes = entry.target.classList;
      if (classes.contains("slider-left-id")) {
        entry.target.classList.add('slide-in-left')
      }
      if (classes.contains("slider-top-id")) {
        entry.target.classList.add('slide-in-top')
      }
      if (classes.contains("aumenta-id")) {
        entry.target.classList.add('aumenta')
      }
    }
    
    }

  
  ))
  const hiddenElements = document.querySelectorAll('.sliders')
  hiddenElements.forEach((el) => observer.observe(el))

