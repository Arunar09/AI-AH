// Web Interface JavaScript
let currentStep = 1;
let selectedProjectType = null;
let requirements = [];
let currentRequirements = [];
let projectData = {};
let currentAgentResponse = null;
let currentScalingPlan = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Project type selection
    document.querySelectorAll('.project-type-card').forEach(card => {
        card.addEventListener('click', function() {
            selectProjectType(this.dataset.type);
        });
    });

    // Step navigation
    document.getElementById('next-step1').addEventListener('click', nextStep);
    document.getElementById('prev-step2').addEventListener('click', prevStep);
    document.getElementById('next-step2').addEventListener('click', processRequirements);
}

function startNewProject() {
    document.getElementById('project-creation').style.display = 'block';
    document.getElementById('project-creation').scrollIntoView({ behavior: 'smooth' });
    resetSteps();
}

function resetSteps() {
    currentStep = 1;
    selectedProjectType = null;
    requirements = [];
    currentRequirements = [];
    projectData = {};
    
    // Reset step indicators
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active', 'completed');
    });
    document.getElementById('step-1').classList.add('active');
    
    // Show step 1 content
    showStep(1);
}

function selectProjectType(type) {
    selectedProjectType = type;
    
    // Update UI
    document.querySelectorAll('.project-type-card').forEach(card => {
        card.classList.remove('border-primary');
    });
    document.querySelector(`[data-type="${type}"]`).classList.add('border-primary');
    
    // Enable next button
    document.getElementById('next-step1').disabled = false;
}

function nextStep() {
    if (currentStep === 1 && selectedProjectType) {
        loadRequirements();
        showStep(2);
    }
}

function prevStep() {
    if (currentStep === 2) {
        showStep(1);
    }
}

function showStep(step) {
    // Hide all step contents
    document.querySelectorAll('[id$="-content"]').forEach(content => {
        content.style.display = 'none';
    });
    
    // Update step indicators
    document.querySelectorAll('.step').forEach(stepEl => {
        stepEl.classList.remove('active', 'completed');
    });
    
    for (let i = 1; i <= step; i++) {
        if (i < step) {
            document.getElementById(`step-${i}`).classList.add('completed');
        } else {
            document.getElementById(`step-${i}`).classList.add('active');
        }
    }
    
    // Show current step content
    document.getElementById(`step${step}-content`).style.display = 'block';
    currentStep = step;
}

async function loadRequirements() {
    try {
        const response = await fetch(`/requirements/${selectedProjectType}`);
        const data = await response.json();
        currentRequirements = data.requirements;
        renderRequirements();
    } catch (error) {
        console.error('Error loading requirements:', error);
        showAlert('Error loading requirements', 'danger');
    }
}

function renderRequirements() {
    const container = document.getElementById('requirements-container');
    container.innerHTML = '';
    
    currentRequirements.forEach((req, index) => {
        const requirementDiv = document.createElement('div');
        requirementDiv.className = 'mb-4';
        requirementDiv.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">${req.question}</h6>
                    ${renderRequirementInput(req, index)}
                    <div class="invalid-feedback" id="feedback-${index}"></div>
                </div>
            </div>
        `;
        container.appendChild(requirementDiv);
    });
    
    // Add event listeners for validation
    addValidationListeners();
}

function renderRequirementInput(req, index) {
    const inputId = `req-${index}`;
    const rulesJson = JSON.stringify(req.validation_rules).replace(/"/g, '&quot;');
    
    switch (req.type) {
        case 'dropdown':
            return `
                <select class="form-select" id="${inputId}" data-index="${index}" data-rules="${rulesJson}">
                    <option value="">Select an option...</option>
                    ${req.options.map(option => `<option value="${option}">${option}</option>`).join('')}
                </select>
            `;
        case 'textarea':
            return `
                <textarea class="form-control" id="${inputId}" data-index="${index}" data-rules="${rulesJson}" rows="3" placeholder="Enter your answer..."></textarea>
            `;
        case 'number':
            return `
                <input type="number" class="form-control" id="${inputId}" data-index="${index}" data-rules="${rulesJson}" placeholder="Enter a number...">
            `;
        default:
            return `
                <input type="text" class="form-control" id="${inputId}" data-index="${index}" data-rules="${rulesJson}" placeholder="Enter your answer...">
            `;
    }
}

function addValidationListeners() {
    document.querySelectorAll('[data-index]').forEach(input => {
        input.addEventListener('input', function() {
            validateRequirement(this);
            updateProgress();
            checkNextButton();
        });
    });
}

async function validateRequirement(input) {
    const index = input.dataset.index;
    const answer = input.value.trim();
    
    // Parse rules safely
    let rules = [];
    try {
        const rulesStr = input.dataset.rules.replace(/&quot;/g, '"');
        rules = JSON.parse(rulesStr);
    } catch (error) {
        console.error('Error parsing validation rules:', error);
        return false;
    }
    
    try {
        const response = await fetch('/validate-requirement', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                answer: answer,
                validation_rules: rules
            })
        });
        
        const data = await response.json();
        const feedback = document.getElementById(`feedback-${index}`);
        
        if (data.is_valid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            feedback.textContent = '';
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            feedback.textContent = data.message;
        }
        
        return data.is_valid;
    } catch (error) {
        console.error('Validation error:', error);
        return false;
    }
}

function updateProgress() {
    const totalRequirements = currentRequirements.length;
    const completedRequirements = document.querySelectorAll('.is-valid').length;
    const progress = (completedRequirements / totalRequirements) * 100;
    
    document.getElementById('requirements-progress').style.width = `${progress}%`;
    document.getElementById('requirements-progress').textContent = `${Math.round(progress)}%`;
}

function checkNextButton() {
    const totalRequirements = currentRequirements.length;
    const completedRequirements = document.querySelectorAll('.is-valid').length;
    
    document.getElementById('next-step2').disabled = completedRequirements < totalRequirements;
}

async function processRequirements() {
    // Collect all requirement answers
    const requirementAnswers = [];
    document.querySelectorAll('[data-index]').forEach(input => {
        const index = parseInt(input.dataset.index);
        const requirement = currentRequirements[index];
        requirementAnswers.push({
            category: requirement.category,
            question: requirement.question,
            answer: input.value.trim(),
            validation_rules: requirement.validation_rules
        });
    });
    
    projectData = {
        project_type: selectedProjectType,
        requirements: requirementAnswers
    };
    
    showStep(3);
    
    try {
        const response = await fetch('/process-requirements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(projectData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAgentResponse = data.response;
            displayProcessingResults(data.response);
            generateScalingPlan();
        } else {
            showAlert(data.error || 'Processing failed', 'danger');
        }
    } catch (error) {
        console.error('Processing error:', error);
        showAlert('Error processing requirements', 'danger');
    }
}

function displayProcessingResults(response) {
    const resultsContainer = document.getElementById('processing-results');
    resultsContainer.innerHTML = `
        <div class="result-card">
            <h4 class="text-success">
                <i class="fas fa-check-circle me-2"></i>
                Infrastructure Plan Generated!
            </h4>
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Cost Estimate</h6>
                            <h4 class="text-primary">$${response.cost_estimate}/month</h4>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Confidence</h6>
                            <h4 class="text-success">${Math.round(response.confidence * 100)}%</h4>
                        </div>
                    </div>
                </div>
            </div>
            
            ${response.reasoning_steps && response.reasoning_steps.length > 0 ? `
            <div class="mt-4">
                <h6><i class="fas fa-brain me-2"></i>AI Reasoning Analysis:</h6>
                <div class="accordion" id="reasoningAccordion">
                    ${response.reasoning_steps.map((step, index) => `
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="reasoningHeading${index}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#reasoningCollapse${index}">
                                    Step ${index + 1}: ${step.split(':')[0] || step.substring(0, 50)}...
                                </button>
                            </h2>
                            <div id="reasoningCollapse${index}" class="accordion-collapse collapse" data-bs-parent="#reasoningAccordion">
                                <div class="accordion-body">
                                    ${step}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            ${response.design_plan ? `
            <div class="mt-4">
                <h6><i class="fas fa-drafting-compass me-2"></i>Architectural Design Plan:</h6>
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>🏗️ Architecture Pattern</h6>
                                <p><strong>${response.design_plan.architecture_pattern?.pattern || 'N/A'}</strong></p>
                                <p>${response.design_plan.architecture_pattern?.description || 'N/A'}</p>
                                <small class="text-muted">${response.design_plan.architecture_pattern?.rationale || 'N/A'}</small>
                            </div>
                            <div class="col-md-6">
                                <h6>🔧 Components</h6>
                                <ul class="list-unstyled">
                                    ${response.design_plan.components ? Object.entries(response.design_plan.components).map(([category, items]) => 
                                        `<li><strong>${category}:</strong> ${Object.keys(items).join(', ')}</li>`
                                    ).join('') : '<li>N/A</li>'}
                                </ul>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-4">
                                <h6>🌐 Networking</h6>
                                <ul class="list-unstyled">
                                    ${response.design_plan.networking ? Object.entries(response.design_plan.networking).map(([key, value]) => 
                                        `<li><strong>${key}:</strong> ${typeof value === 'object' ? JSON.stringify(value, null, 2) : value}</li>`
                                    ).join('') : '<li>N/A</li>'}
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>🔒 Security</h6>
                                <ul class="list-unstyled">
                                    ${response.design_plan.security ? Object.entries(response.design_plan.security).map(([key, value]) => 
                                        `<li><strong>${key}:</strong> ${typeof value === 'object' ? JSON.stringify(value, null, 2) : value}</li>`
                                    ).join('') : '<li>N/A</li>'}
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>📊 Monitoring</h6>
                                <ul class="list-unstyled">
                                    ${response.design_plan.monitoring ? Object.entries(response.design_plan.monitoring).map(([key, value]) => 
                                        `<li><strong>${key}:</strong> ${typeof value === 'object' ? JSON.stringify(value, null, 2) : value}</li>`
                                    ).join('') : '<li>N/A</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ` : ''}
            
            ${response.implementation_plan ? `
            <div class="mt-4">
                <h6><i class="fas fa-tasks me-2"></i>Implementation Plan:</h6>
                <div class="accordion" id="implementationAccordion">
                    ${response.implementation_plan.phases ? response.implementation_plan.phases.map((phase, index) => `
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="phaseHeading${index}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#phaseCollapse${index}">
                                    ${phase.phase} (${phase.duration}) - Risk: ${phase.risk_level}
                                </button>
                            </h2>
                            <div id="phaseCollapse${index}" class="accordion-collapse collapse" data-bs-parent="#implementationAccordion">
                                <div class="accordion-body">
                                    <p>${phase.description}</p>
                                    <h6>Steps:</h6>
                                    <ol>
                                        ${phase.steps.map(step => `<li>${step}</li>`).join('')}
                                    </ol>
                                    ${phase.dependencies.length > 0 ? `<p><strong>Dependencies:</strong> ${phase.dependencies.join(', ')}</p>` : ''}
                                </div>
                            </div>
                        </div>
                    `).join('') : '<p>No implementation phases available</p>'}
                </div>
                
                <div class="row mt-3">
                    <div class="col-md-6">
                        <h6>🔄 Rollback Strategy</h6>
                        <ul>
                            ${response.implementation_plan.rollback_strategy ? response.implementation_plan.rollback_strategy.rollback_steps.map(step => 
                                `<li>${step}</li>`
                            ).join('') : '<li>N/A</li>'}
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6>✅ Success Criteria</h6>
                        <ul>
                            ${response.implementation_plan.success_criteria ? response.implementation_plan.success_criteria.map(criteria => 
                                `<li>${criteria}</li>`
                            ).join('') : '<li>N/A</li>'}
                        </ul>
                    </div>
                </div>
            </div>
            ` : ''}
            
            <div class="mt-4">
                <h6><i class="fas fa-cogs me-2"></i>Implementation Steps:</h6>
                <ol>
                    ${response.implementation_steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
            </div>
            
            <div class="mt-4">
                <h6><i class="fas fa-file-code me-2"></i>Generated Terraform Files:</h6>
                <div class="row">
                    ${Object.entries(response.terraform_code).map(([filename, content]) => `
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-header">
                                    <h6 class="mb-0"><code>${filename}</code></h6>
                                </div>
                                <div class="card-body">
                                    <div class="code-block" style="max-height: 200px;">
                                        <pre><code>${content.substring(0, 500)}${content.length > 500 ? '...' : ''}</code></pre>
                                    </div>
                                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="downloadFile('${filename}', \`${content.replace(/`/g, '\\`')}\`)">
                                        <i class="fas fa-download me-1"></i>Download
                                    </button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            ${response.content ? `
            <div class="mt-4">
                <h6><i class="fas fa-lightbulb me-2"></i>Detailed Analysis:</h6>
                <div class="alert alert-info">
                    ${response.content}
                </div>
            </div>
            ` : ''}
            
            <div class="mt-4">
                <h6><i class="fas fa-folder-plus me-2"></i>Create Project Workspace:</h6>
                <div class="row">
                    <div class="col-md-8">
                        <input type="text" class="form-control" id="project-name" placeholder="Enter project name..." value="${projectData.requirements.find(r => r.category === 'basic_info')?.answer || 'My Project'}">
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-success w-100" onclick="createWorkspace()">
                            <i class="fas fa-folder-plus me-2"></i>Create Workspace
                        </button>
                    </div>
                </div>
                <div id="workspace-status" class="mt-2"></div>
            </div>
        </div>
    `;
    resultsContainer.style.display = 'block';
}

async function generateScalingPlan() {
    try {
        const response = await fetch('/generate-scaling-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(projectData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentScalingPlan = data.scaling_plan;
            displayScalingPlan(data.scaling_plan);
            showStep(4);
        } else {
            showAlert(data.error || 'Scaling plan generation failed', 'danger');
        }
    } catch (error) {
        console.error('Scaling plan error:', error);
        showAlert('Error generating scaling plan', 'danger');
    }
}

function displayScalingPlan(scalingPlan) {
    const container = document.getElementById('scaling-plan-results');
    container.innerHTML = `
        <div class="result-card">
            <h4 class="text-primary">
                <i class="fas fa-chart-line me-2"></i>
                Production Scaling Plan
            </h4>
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Estimated Duration</h6>
                            <h5 class="text-info">${scalingPlan.estimated_duration}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Current State</h6>
                            <h5 class="text-warning">${scalingPlan.current_state}</h5>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <h6>Deployment Phases:</h6>
                <div class="accordion" id="phasesAccordion">
                    ${scalingPlan.phases.map((phase, index) => `
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="heading${index}">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                    Phase ${index + 1}: ${phase.name} (${phase.duration})
                                </button>
                            </h2>
                            <div id="collapse${index}" class="accordion-collapse collapse" data-bs-parent="#phasesAccordion">
                                <div class="accordion-body">
                                    <ul>
                                        ${phase.steps.map(step => `<li>${step}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="row mt-4">
                <div class="col-md-6">
                    <h6>Cost Implications:</h6>
                    <ul>
                        ${Object.entries(scalingPlan.cost_implications).map(([key, value]) => 
                            `<li><strong>${key.replace('_', ' ').toUpperCase()}:</strong> ${value}</li>`
                        ).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>Risk Assessment:</h6>
                    <ul>
                        ${scalingPlan.risk_assessment.map(risk => `<li>${risk}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
}

function downloadProject() {
    const projectJson = JSON.stringify(projectData, null, 2);
    const blob = new Blob([projectJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${projectData.project_type}_project.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function showTroubleshooting(category) {
    // This would open a troubleshooting modal or navigate to a troubleshooting page
    alert(`Troubleshooting for ${category} issues would be shown here.`);
}

function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function createWorkspace() {
    const projectName = document.getElementById('project-name').value.trim();
    const statusDiv = document.getElementById('workspace-status');
    
    if (!projectName) {
        statusDiv.innerHTML = '<div class="alert alert-warning">Please enter a project name</div>';
        return;
    }
    
    try {
        statusDiv.innerHTML = '<div class="alert alert-info"><i class="fas fa-spinner fa-spin me-2"></i>Creating workspace...</div>';
        
        const response = await fetch('/create-workspace', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                project_name: projectName,
                terraform_code: currentAgentResponse.terraform_code,
                requirements: projectData,
                scaling_plan: currentScalingPlan
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            statusDiv.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    Workspace created successfully!
                    <div class="mt-2">
                        <button class="btn btn-sm btn-primary me-2" onclick="downloadProject('${projectName}')">
                            <i class="fas fa-download me-1"></i>Download Project
                        </button>
                        <button class="btn btn-sm btn-info" onclick="viewProject('${projectName}')">
                            <i class="fas fa-eye me-1"></i>View Files
                        </button>
                    </div>
                </div>
            `;
        } else {
            statusDiv.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error creating workspace:', error);
        statusDiv.innerHTML = `<div class="alert alert-danger">Error creating workspace: ${error.message}</div>`;
    }
}

async function downloadProject(projectName) {
    try {
        showAlert('Preparing download...', 'info');
        
        const response = await fetch(`/download-project/${encodeURIComponent(projectName)}`);
        
        if (response.ok) {
            const blob = await response.blob();
            
            // Check if we got a valid zip file
            if (blob.size === 0) {
                showAlert('Download failed: Empty file received', 'danger');
                return;
            }
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${projectName}.zip`;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showAlert('Project downloaded successfully!', 'success');
        } else {
            const error = await response.json();
            showAlert(`Error downloading project: ${error.error}`, 'danger');
        }
    } catch (error) {
        console.error('Error downloading project:', error);
        showAlert(`Error downloading project: ${error.message}`, 'danger');
    }
}

async function viewProject(projectName) {
    try {
        const response = await fetch(`/project/${encodeURIComponent(projectName)}`);
        const data = await response.json();
        
        if (data.success) {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Project: ${data.project_name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>Path:</strong> ${data.project_path}</p>
                            <h6>Files:</h6>
                            <div class="list-group">
                                ${data.files.map(file => `
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <span><i class="fas fa-file me-2"></i>${file.path}</span>
                                        <span class="badge bg-secondary">${(file.size / 1024).toFixed(1)} KB</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="downloadProject('${projectName}')">
                                <i class="fas fa-download me-1"></i>Download Project
                            </button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
            
            modal.addEventListener('hidden.bs.modal', () => {
                document.body.removeChild(modal);
            });
        } else {
            showAlert(`Error viewing project: ${data.error}`, 'danger');
        }
    } catch (error) {
        console.error('Error viewing project:', error);
        showAlert(`Error viewing project: ${error.message}`, 'danger');
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}
