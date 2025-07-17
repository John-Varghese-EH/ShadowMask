// ShadowMask Website JavaScript
// Enhanced functionality with Python integration simulation

class ShadowMaskDemo {
    constructor() {
        this.currentStep = 1;
        this.selectedMethods = ['alpha', 'adversarial', 'encoder', 'diffusion', 'metadata'];
        this.currentImage = null;
        this.protectedImage = null;
        this.processingTime = 0;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupIntersectionObserver();
        this.detectUserOS();
        this.startLiveStats();
        this.setupAPITabs();
        this.setupContactForm();
        this.setupImageUpload();
        this.setupProtectionOptions();
        this.setupDemoNavigation();
    }

    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                const icon = mobileMenuBtn.querySelector('i');
                if (mobileMenu.classList.contains('hidden')) {
                    icon.setAttribute('data-lucide', 'menu');
                } else {
                    icon.setAttribute('data-lucide', 'x');
                }
                lucide.createIcons();
            });
        }

        // Navigation links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                this.scrollToSection(targetId);
                
                // Close mobile menu if open
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.setAttribute('data-lucide', 'menu');
                    lucide.createIcons();
                }
            });
        });

        // Back to top button
        const backToTopBtn = document.getElementById('back-to-top');
        if (backToTopBtn) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    backToTopBtn.classList.add('visible');
                    backToTopBtn.style.opacity = '1';
                    backToTopBtn.style.pointerEvents = 'auto';
                } else {
                    backToTopBtn.classList.remove('visible');
                    backToTopBtn.style.opacity = '0';
                    backToTopBtn.style.pointerEvents = 'none';
                }
            });

            backToTopBtn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }

        // Navbar background on scroll
        const navbar = document.getElementById('navbar');
        if (navbar) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 50) {
                    navbar.style.backgroundColor = 'rgba(17, 24, 39, 0.95)';
                } else {
                    navbar.style.backgroundColor = 'rgba(17, 24, 39, 0.8)';
                }
            });
        }
    }

    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    
                    // Update active nav link
                    const id = entry.target.id;
                    document.querySelectorAll('.nav-link').forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === `#${id}`) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }, observerOptions);

        // Observe all sections
        document.querySelectorAll('section[id]').forEach(section => {
            observer.observe(section);
        });
    }

    scrollToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            const offsetTop = element.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }

    detectUserOS() {
        const platform = navigator.platform.toLowerCase();
        const userAgent = navigator.userAgent.toLowerCase();
        
        let os = 'Unknown';
        let icon = 'monitor';
        
        if (platform.includes('win')) {
            os = 'Windows';
            icon = 'monitor';
        } else if (platform.includes('mac')) {
            os = 'macOS';
            icon = 'apple';
        } else if (platform.includes('linux')) {
            os = 'Linux';
            icon = 'terminal';
        } else if (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent)) {
            os = 'Android';
            icon = 'smartphone';
        }

        // Update recommended download section
        const recommendedIcon = document.getElementById('recommended-icon');
        const recommendedTitle = document.getElementById('recommended-title');
        
        if (recommendedIcon && recommendedTitle) {
            recommendedIcon.setAttribute('data-lucide', icon);
            recommendedTitle.textContent = `ShadowMask for ${os}`;
            lucide.createIcons();
        }
    }

    startLiveStats() {
        const imagesProtected = document.getElementById('images-protected');
        const aiBlocks = document.getElementById('ai-blocks');
        const privacyScore = document.getElementById('privacy-score');

        if (imagesProtected && aiBlocks && privacyScore) {
            // Animate counters
            this.animateCounter(imagesProtected, 0, 15847, 2000);
            this.animateCounter(aiBlocks, 0, 99, 1500);
            
            // Keep privacy score at 100%
            privacyScore.textContent = '100%';
        }
    }

    animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        
        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (end - start) * progress);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        };
        
        requestAnimationFrame(updateCounter);
    }

    setupAPITabs() {
        const tabButtons = document.querySelectorAll('.api-tab-btn');
        const tabContents = document.querySelectorAll('.api-tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Update button states
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Update content visibility
                tabContents.forEach(content => {
                    if (content.id === `api-${targetTab}`) {
                        content.classList.remove('hidden');
                    } else {
                        content.classList.add('hidden');
                    }
                });
            });
        });
    }

    setupContactForm() {
        const contactForm = document.getElementById('contact-form');
        const contactStatus = document.getElementById('contact-status');
        const submitBtn = document.getElementById('contact-submit');
        const submitText = document.getElementById('submit-text');
        const submitIcon = document.getElementById('submit-icon');

        if (contactForm) {
            contactForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Show loading state
                submitBtn.disabled = true;
                submitText.textContent = 'Sending...';
                submitIcon.setAttribute('data-lucide', 'loader');
                submitIcon.classList.add('animate-spin');
                lucide.createIcons();

                // Simulate form submission
                try {
                    await this.simulateFormSubmission();
                    
                    // Show success message
                    this.showContactStatus('success', 'Message sent successfully! We\'ll get back to you soon.');
                    contactForm.reset();
                    
                } catch (error) {
                    // Show error message
                    this.showContactStatus('error', 'Failed to send message. Please try again later.');
                } finally {
                    // Reset button state
                    submitBtn.disabled = false;
                    submitText.textContent = 'Send Message';
                    submitIcon.setAttribute('data-lucide', 'send');
                    submitIcon.classList.remove('animate-spin');
                    lucide.createIcons();
                }
            });
        }
    }

    showContactStatus(type, message) {
        const contactStatus = document.getElementById('contact-status');
        if (contactStatus) {
            contactStatus.className = `mb-6 p-4 rounded-lg ${type === 'success' ? 'bg-green-900/20 border border-green-500/30 text-green-400' : 'bg-red-900/20 border border-red-500/30 text-red-400'}`;
            contactStatus.textContent = message;
            contactStatus.classList.remove('hidden');
            
            // Hide after 5 seconds
            setTimeout(() => {
                contactStatus.classList.add('hidden');
            }, 5000);
        }
    }

    async simulateFormSubmission() {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulate 90% success rate
                if (Math.random() > 0.1) {
                    resolve();
                } else {
                    reject(new Error('Simulated error'));
                }
            }, 2000);
        });
    }

    setupImageUpload() {
        const uploadArea = document.getElementById('upload-area');
        const imageInput = document.getElementById('image-input');
        const uploadContent = document.getElementById('upload-content');
        const uploadPreview = document.getElementById('upload-preview');
        const previewImage = document.getElementById('preview-image');

        if (uploadArea && imageInput) {
            // Click to upload
            uploadArea.addEventListener('click', () => {
                imageInput.click();
            });

            // File input change
            imageInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.handleImageUpload(file);
                }
            });

            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    this.handleImageUpload(file);
                }
            });
        }
    }

    handleImageUpload(file) {
        const uploadContent = document.getElementById('upload-content');
        const uploadPreview = document.getElementById('upload-preview');
        const previewImage = document.getElementById('preview-image');
        const nextBtn = document.getElementById('demo-next-btn');

        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.currentImage = e.target.result;
                previewImage.src = e.target.result;
                uploadContent.classList.add('hidden');
                uploadPreview.classList.remove('hidden');
                
                // Enable next button
                if (nextBtn) {
                    nextBtn.disabled = false;
                }
            };
            reader.readAsDataURL(file);
        }
    }

    loadSampleImage(imageUrl) {
        const uploadContent = document.getElementById('upload-content');
        const uploadPreview = document.getElementById('upload-preview');
        const previewImage = document.getElementById('preview-image');
        const nextBtn = document.getElementById('demo-next-btn');

        this.currentImage = imageUrl;
        previewImage.src = imageUrl;
        uploadContent.classList.add('hidden');
        uploadPreview.classList.remove('hidden');
        
        // Enable next button
        if (nextBtn) {
            nextBtn.disabled = false;
        }
    }

    setupProtectionOptions() {
        const protectionOptions = document.querySelectorAll('.protection-option');
        const protectionBar = document.getElementById('protection-bar');
        const protectionStrength = document.getElementById('protection-strength');

        protectionOptions.forEach(option => {
            const checkbox = option.querySelector('input[type="checkbox"]');
            
            option.addEventListener('click', (e) => {
                if (e.target.type !== 'checkbox') {
                    checkbox.checked = !checkbox.checked;
                }
                
                if (checkbox.checked) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
                
                this.updateProtectionStrength();
            });

            // Initialize selected state
            if (checkbox.checked) {
                option.classList.add('selected');
            }
        });

        this.updateProtectionStrength();
    }

    updateProtectionStrength() {
        const checkedOptions = document.querySelectorAll('.protection-option input[type="checkbox"]:checked');
        const totalOptions = document.querySelectorAll('.protection-option input[type="checkbox"]');
        const percentage = (checkedOptions.length / totalOptions.length) * 100;
        
        const protectionBar = document.getElementById('protection-bar');
        const protectionStrength = document.getElementById('protection-strength');
        
        if (protectionBar) {
            protectionBar.style.width = `${percentage}%`;
        }
        
        if (protectionStrength) {
            if (percentage >= 80) {
                protectionStrength.textContent = 'Maximum';
                protectionStrength.className = 'text-sm font-medium text-green-400';
            } else if (percentage >= 60) {
                protectionStrength.textContent = 'High';
                protectionStrength.className = 'text-sm font-medium text-purple-400';
            } else if (percentage >= 40) {
                protectionStrength.textContent = 'Medium';
                protectionStrength.className = 'text-sm font-medium text-yellow-400';
            } else {
                protectionStrength.textContent = 'Low';
                protectionStrength.className = 'text-sm font-medium text-red-400';
            }
        }

        // Update selected methods
        this.selectedMethods = Array.from(checkedOptions).map(cb => 
            cb.closest('.protection-option').getAttribute('data-method')
        );
    }

    setupDemoNavigation() {
        const backBtn = document.getElementById('demo-back-btn');
        const nextBtn = document.getElementById('demo-next-btn');

        if (backBtn) {
            backBtn.addEventListener('click', () => {
                this.previousStep();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.nextStep();
            });
        }
    }

    nextStep() {
        if (this.currentStep < 4) {
            if (this.currentStep === 3) {
                this.startProcessing();
            } else {
                this.currentStep++;
                this.updateDemoStep();
            }
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateDemoStep();
        }
    }

    updateDemoStep() {
        // Update step indicators
        for (let i = 1; i <= 4; i++) {
            const stepElement = document.getElementById(`step-${i}`);
            const progressElement = document.getElementById(`progress-${i}`);
            
            if (stepElement) {
                if (i <= this.currentStep) {
                    stepElement.className = 'flex items-center justify-center w-8 h-8 rounded-full bg-purple-600 text-white text-sm font-medium';
                } else {
                    stepElement.className = 'flex items-center justify-center w-8 h-8 rounded-full bg-gray-700 text-gray-400 text-sm font-medium';
                }
            }
            
            if (progressElement && i < 4) {
                if (i < this.currentStep) {
                    progressElement.className = 'flex-1 h-1 mx-2 bg-purple-600';
                } else {
                    progressElement.className = 'flex-1 h-1 mx-2 bg-gray-700';
                }
            }
        }

        // Update step content
        document.querySelectorAll('.demo-step').forEach((step, index) => {
            if (index + 1 === this.currentStep) {
                step.classList.remove('hidden');
            } else {
                step.classList.add('hidden');
            }
        });

        // Update navigation buttons
        const backBtn = document.getElementById('demo-back-btn');
        const nextBtn = document.getElementById('demo-next-btn');
        const navigation = document.getElementById('demo-navigation');

        if (backBtn) {
            backBtn.disabled = this.currentStep === 1;
        }

        if (nextBtn) {
            if (this.currentStep === 1) {
                nextBtn.disabled = !this.currentImage;
            } else if (this.currentStep === 3) {
                nextBtn.textContent = 'Apply Protection';
                nextBtn.innerHTML = 'Apply Protection <i data-lucide="zap" class="h-4 w-4 ml-2 inline"></i>';
                lucide.createIcons();
            } else if (this.currentStep === 4) {
                navigation.classList.add('hidden');
            } else {
                nextBtn.disabled = false;
                nextBtn.innerHTML = 'Next <i data-lucide="arrow-right" class="h-4 w-4 ml-2 inline"></i>';
                lucide.createIcons();
            }
        }
    }

    async startProcessing() {
        this.currentStep = 3;
        this.updateDemoStep();

        const processingSteps = document.querySelectorAll('.processing-step');
        const processingBar = document.getElementById('processing-bar');
        const processingPercentage = document.getElementById('processing-percentage');
        const processingTime = document.getElementById('processing-time');

        const startTime = Date.now();

        // Simulate processing steps
        const steps = [
            { text: 'Analyzing image structure...', duration: 800 },
            { text: 'Applying protection methods...', duration: 1200 },
            { text: 'Optimizing output...', duration: 600 },
            { text: 'Finalizing protection...', duration: 400 }
        ];

        let totalProgress = 0;
        const progressIncrement = 100 / steps.length;

        for (let i = 0; i < steps.length; i++) {
            const step = processingSteps[i];
            if (step) {
                // Activate current step
                step.classList.add('active');
                step.classList.remove('opacity-50');
                
                // Update step text
                const stepText = step.querySelector('span');
                if (stepText) {
                    stepText.textContent = steps[i].text;
                }
            }

            // Animate progress
            await this.animateProgress(processingBar, processingPercentage, totalProgress, totalProgress + progressIncrement, steps[i].duration);
            totalProgress += progressIncrement;

            // Complete current step
            if (step) {
                step.classList.remove('active');
                step.classList.add('completed');
            }
        }

        // Calculate processing time
        this.processingTime = ((Date.now() - startTime) / 1000).toFixed(1);
        if (processingTime) {
            processingTime.textContent = `${this.processingTime}s`;
        }

        // Generate protected image
        await this.generateProtectedImage();

        // Move to results step
        this.currentStep = 4;
        this.updateDemoStep();
        this.showResults();
    }

    async animateProgress(progressBar, percentageElement, startPercent, endPercent, duration) {
        return new Promise(resolve => {
            const startTime = Date.now();
            
            const updateProgress = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const currentPercent = startPercent + (endPercent - startPercent) * progress;
                
                if (progressBar) {
                    progressBar.style.width = `${currentPercent}%`;
                }
                
                if (percentageElement) {
                    percentageElement.textContent = `${Math.round(currentPercent)}%`;
                }
                
                if (progress < 1) {
                    requestAnimationFrame(updateProgress);
                } else {
                    resolve();
                }
            };
            
            requestAnimationFrame(updateProgress);
        });
    }

    async generateProtectedImage() {
        // Simulate image protection using canvas manipulation
        const canvas = document.getElementById('protected-result');
        const originalResult = document.getElementById('original-result');
        
        if (canvas && this.currentImage) {
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            return new Promise(resolve => {
                img.onload = () => {
                    // Set canvas size
                    canvas.width = img.width;
                    canvas.height = img.height;
                    
                    // Draw original image
                    ctx.drawImage(img, 0, 0);
                    
                    // Apply simulated protection effects
                    this.applyProtectionEffects(ctx, canvas.width, canvas.height);
                    
                    // Set original image
                    if (originalResult) {
                        originalResult.src = this.currentImage;
                    }
                    
                    resolve();
                };
                img.src = this.currentImage;
            });
        }
    }

    applyProtectionEffects(ctx, width, height) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;

        // Apply subtle noise (simulating adversarial patterns)
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < 0.1) { // 10% of pixels
                const noise = (Math.random() - 0.5) * 10;
                data[i] = Math.max(0, Math.min(255, data[i] + noise));     // Red
                data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + noise)); // Green
                data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + noise)); // Blue
            }
        }

        // Apply alpha channel modifications (simulating alpha layer attacks)
        if (this.selectedMethods.includes('alpha')) {
            for (let i = 3; i < data.length; i += 4) {
                if (Math.random() < 0.05) { // 5% of pixels
                    data[i] = Math.max(200, data[i]); // Modify alpha
                }
            }
        }

        ctx.putImageData(imageData, 0, 0);

        // Add subtle overlay to indicate protection
        ctx.fillStyle = 'rgba(93, 63, 211, 0.02)';
        ctx.fillRect(0, 0, width, height);
    }

    showResults() {
        const methodsApplied = document.getElementById('methods-applied');
        const downloadBtn = document.getElementById('download-protected');

        if (methodsApplied) {
            methodsApplied.textContent = this.selectedMethods.length;
        }

        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                this.downloadProtectedImage();
            });
        }
    }

    downloadProtectedImage() {
        const canvas = document.getElementById('protected-result');
        if (canvas) {
            const link = document.createElement('a');
            link.download = 'shadowmask-protected-image.png';
            link.href = canvas.toDataURL();
            link.click();
        }
    }

    resetDemo() {
        this.currentStep = 1;
        this.currentImage = null;
        this.protectedImage = null;
        
        // Reset UI elements
        const uploadContent = document.getElementById('upload-content');
        const uploadPreview = document.getElementById('upload-preview');
        const navigation = document.getElementById('demo-navigation');
        
        if (uploadContent) uploadContent.classList.remove('hidden');
        if (uploadPreview) uploadPreview.classList.add('hidden');
        if (navigation) navigation.classList.remove('hidden');
        
        // Reset processing steps
        document.querySelectorAll('.processing-step').forEach(step => {
            step.classList.remove('active', 'completed');
            step.classList.add('opacity-50');
        });
        
        // Reset progress
        const processingBar = document.getElementById('processing-bar');
        const processingPercentage = document.getElementById('processing-percentage');
        
        if (processingBar) processingBar.style.width = '0%';
        if (processingPercentage) processingPercentage.textContent = '0%';
        
        this.updateDemoStep();
    }
}

// Global functions for HTML onclick handlers
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        const offsetTop = element.offsetTop - 80;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

function loadSampleImage(imageUrl) {
    if (window.shadowMaskDemo) {
        window.shadowMaskDemo.loadSampleImage(imageUrl);
    }
}

function resetDemo() {
    if (window.shadowMaskDemo) {
        window.shadowMaskDemo.resetDemo();
    }
}

// Enhanced Image Protection Simulation
class ImageProtectionEngine {
    constructor() {
        this.methods = {
            alpha_attack: this.applyAlphaAttack,
            adversarial: this.applyAdversarialPatterns,
            encoder: this.applyEncoderAttack,
            diffusion: this.applyDiffusionAttack,
            metadata: this.applyMetadataProtection,
            steganography: this.applySteganography
        };
    }

    async protectImage(imageData, selectedMethods, strength = 0.8) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        return new Promise(resolve => {
            const img = new Image();
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                
                // Apply selected protection methods
                selectedMethods.forEach(method => {
                    if (this.methods[method]) {
                        this.methods[method].call(this, ctx, canvas.width, canvas.height, strength);
                    }
                });
                
                resolve(canvas.toDataURL());
            };
            img.src = imageData;
        });
    }

    applyAlphaAttack(ctx, width, height, strength) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        for (let i = 3; i < data.length; i += 4) {
            if (Math.random() < strength * 0.1) {
                data[i] = Math.max(200, data[i] - Math.random() * 20);
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applyAdversarialPatterns(ctx, width, height, strength) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < strength * 0.05) {
                const noise = (Math.random() - 0.5) * strength * 15;
                data[i] = Math.max(0, Math.min(255, data[i] + noise));
                data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + noise));
                data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + noise));
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applyEncoderAttack(ctx, width, height, strength) {
        // Simulate encoder attack with frequency domain modifications
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        // Apply subtle color space modifications
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < strength * 0.02) {
                const shift = Math.sin(i * 0.001) * strength * 5;
                data[i] = Math.max(0, Math.min(255, data[i] + shift));
                data[i + 1] = Math.max(0, Math.min(255, data[i + 1] - shift));
                data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + shift));
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applyDiffusionAttack(ctx, width, height, strength) {
        // Simulate diffusion attack with gradient modifications
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                if (Math.random() < strength * 0.01) {
                    const idx = (y * width + x) * 4;
                    const gradient = Math.random() * strength * 3;
                    
                    data[idx] = Math.max(0, Math.min(255, data[idx] + gradient));
                    data[idx + 1] = Math.max(0, Math.min(255, data[idx + 1] + gradient));
                    data[idx + 2] = Math.max(0, Math.min(255, data[idx + 2] + gradient));
                }
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applyMetadataProtection(ctx, width, height, strength) {
        // Simulate metadata embedding (visual indicator only)
        ctx.fillStyle = `rgba(93, 63, 211, ${strength * 0.01})`;
        ctx.fillRect(0, 0, width, height);
    }

    applySteganography(ctx, width, height, strength) {
        // Simulate steganographic data hiding
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < strength * 0.001) {
                // Modify LSB
                data[i] = (data[i] & 0xFE) | Math.round(Math.random());
                data[i + 1] = (data[i + 1] & 0xFE) | Math.round(Math.random());
                data[i + 2] = (data[i + 2] & 0xFE) | Math.round(Math.random());
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            interactionTime: 0
        };
        
        this.startTime = performance.now();
        this.init();
    }

    init() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            this.metrics.loadTime = performance.now() - this.startTime;
            this.reportMetrics();
        });

        // Monitor interaction performance
        document.addEventListener('click', (e) => {
            const startTime = performance.now();
            requestAnimationFrame(() => {
                this.metrics.interactionTime = performance.now() - startTime;
            });
        });
    }

    reportMetrics() {
        if (window.gtag) {
            window.gtag('event', 'performance', {
                'load_time': this.metrics.loadTime,
                'render_time': this.metrics.renderTime,
                'interaction_time': this.metrics.interactionTime
            });
        }
    }
}

// Accessibility Manager
class AccessibilityManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupKeyboardNavigation();
        this.setupScreenReaderSupport();
        this.setupFocusManagement();
        this.setupReducedMotion();
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Escape key closes modals/menus
            if (e.key === 'Escape') {
                const mobileMenu = document.getElementById('mobile-menu');
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                }
            }

            // Tab navigation enhancement
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    setupScreenReaderSupport() {
        // Add ARIA labels and descriptions
        const interactiveElements = document.querySelectorAll('button, a, input, select, textarea');
        interactiveElements.forEach(element => {
            if (!element.getAttribute('aria-label') && !element.getAttribute('aria-labelledby')) {
                const text = element.textContent || element.value || element.placeholder;
                if (text) {
                    element.setAttribute('aria-label', text.trim());
                }
            }
        });
    }

    setupFocusManagement() {
        // Ensure focus is visible
        const style = document.createElement('style');
        style.textContent = `
            .keyboard-navigation *:focus {
                outline: 2px solid #5D3FD3 !important;
                outline-offset: 2px !important;
            }
        `;
        document.head.appendChild(style);
    }

    setupReducedMotion() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.style.setProperty('--animation-duration', '0.01ms');
            document.documentElement.style.setProperty('--transition-duration', '0.01ms');
        }
    }
}

// Error Handler
class ErrorHandler {
    constructor() {
        this.init();
    }

    init() {
        window.addEventListener('error', (e) => {
            this.logError('JavaScript Error', e.error);
        });

        window.addEventListener('unhandledrejection', (e) => {
            this.logError('Unhandled Promise Rejection', e.reason);
        });
    }

    logError(type, error) {
        console.error(`${type}:`, error);
        
        // Report to analytics if available
        if (window.gtag) {
            window.gtag('event', 'exception', {
                'description': `${type}: ${error.message || error}`,
                'fatal': false
            });
        }
    }

    showUserFriendlyError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-900/20 border border-red-500/30 text-red-400 p-4 rounded-lg z-50';
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main demo
    window.shadowMaskDemo = new ShadowMaskDemo();
    
    // Initialize additional managers
    window.imageProtectionEngine = new ImageProtectionEngine();
    window.performanceMonitor = new PerformanceMonitor();
    window.accessibilityManager = new AccessibilityManager();
    window.errorHandler = new ErrorHandler();
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export for global access
window.ShadowMaskDemo = ShadowMaskDemo;
window.ImageProtectionEngine = ImageProtectionEngine;