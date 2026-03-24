$(document).ready(function() {
    // 1. Input Validation and Submission Handling
    $('#generatorForm').on('submit', function(e) {
        let isValid = true;
        
        const topic = $('#topic').val();
        const difficulty = $('#difficulty').val();
        const numQuestions = $('#num_questions').val();

        // Validate rules constraint (not empty & valid boundary)
        if (!topic || !difficulty || !numQuestions || numQuestions < 1 || numQuestions > 10) {
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Prevent form submission
            // Show custom fade-in validation Bootstrap alert 
            $('#errorMsg')
                .removeClass('d-none')
                .css('opacity', 0)
                .animate({ opacity: 1 }, 300);
                
            // Auto hide after 4.5 seconds to clean UI
            setTimeout(() => {
                $('#errorMsg').animate({ opacity: 0 }, 300, function() {
                    $(this).addClass('d-none');
                });
            }, 4500);
        } else {
            // 2. Beautiful Loading Animation Control
            $('#errorMsg').addClass('d-none');
            
            const $btn = $('#generateBtn');
            $btn.prop('disabled', true);
            $btn.find('.btn-text').addClass('d-none');
            $btn.find('.spinner-border').removeClass('d-none');
            // Adding a slight pulsing animation via Bootstrap utility classes could be done here iteratively
            $btn.find('.loading-text').removeClass('d-none');
            
            // Allow native form submission to /generate to continue
        }
    });

    // Toggle Answer functionality for single questions
    $('.toggle-answer-btn').on('click', function() {
        const $btn = $(this);
        const $answerSection = $btn.siblings('.answer-section');
        
        // Use smooth slide toggle animation
        $answerSection.slideToggle(300, function() {
            if ($answerSection.is(':visible')) {
                $btn.text('Hide Answer');
                $btn.removeClass('btn-outline-secondary').addClass('btn-secondary');
            } else {
                $btn.text('Show Answer');
                $btn.removeClass('btn-secondary').addClass('btn-outline-secondary');
            }
        });
    });

    // 3. "Show All Answers" Bulk Toggle Feature
    let allAnswersVisible = false;
    $('#toggleAllAnswersBtn').on('click', function() {
        allAnswersVisible = !allAnswersVisible;
        const $btn = $(this);
        
        if (allAnswersVisible) {
            $('.answer-section').slideDown(300);
            $('.toggle-answer-btn').text('Hide Answer').removeClass('btn-outline-secondary').addClass('btn-secondary');
            $btn.text('Hide All Answers');
        } else {
            $('.answer-section').slideUp(300);
            $('.toggle-answer-btn').text('Show Answer').removeClass('btn-secondary').addClass('btn-outline-secondary');
            $btn.text('Show All Answers');
        }
    });

    // 6. Mock Interview Mode Timer Functionality
    let timerInterval;
    $('#startTimerBtn').on('click', function() {
        const $btn = $(this);
        const $display = $('#timerDisplay');
        const $alertContainer = $('#alertContainer'); 
        
        if ($btn.text() === 'Start' || $btn.text() === 'Resume') {
            $btn.text('Pause').removeClass('btn-outline-success').addClass('btn-outline-warning');
            
            // Ensures answers are hidden when starting timer
            if(allAnswersVisible) {
                $('#toggleAllAnswersBtn').click();
            }

            let timeParts = $display.text().split(':');
            let totalSeconds = parseInt(timeParts[0]) * 60 + parseInt(timeParts[1]);
            
            timerInterval = setInterval(function() {
                if (totalSeconds <= 0) {
                    clearInterval(timerInterval);
                    $btn.text('Time Up!');
                    $btn.removeClass('btn-outline-warning').addClass('btn-danger').prop('disabled', true);
                    
                    // Display Bootstrap Dismissible Alert upon ending
                    const alertHtml = `
                    <div class="col-md-10 col-lg-8 w-100 mb-2">
                        <div class="alert alert-danger alert-dismissible fade show shadow-sm border-0 rounded-4" role="alert">
                            <h4 class="alert-heading fw-bold">⏰ Time's Up!</h4>
                            <p class="mb-0">Your mock interview time has expired. Please review and check your answers.</p>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    </div>`;
                    $alertContainer.html(alertHtml).hide().fadeIn(400);
                    return;
                }
                
                totalSeconds--;
                let mins = Math.floor(totalSeconds / 60);
                let secs = totalSeconds % 60;
                $display.text(`${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`);
            }, 1000);
        } else {
            // User paused
            clearInterval(timerInterval);
            $btn.text('Resume').removeClass('btn-outline-warning').addClass('btn-outline-success');
        }
    });
});
