const fs = require('fs');
const path = require('path');

// The navigation HTML from index.html (updated version)
const newNavHTML = `
    <!-- Main Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark main-nav px-0">
        <div class="container-fluid gx-0">
            <a class="navbar-brand d-flex align-items-center me-0" href="index.html">
                <img src="images/2025_07_14_13_42_IMG_2808.PNG" alt="Federal Ministry of Women Affairs Logo" class="fmwa-logo-stretch">
                <span class="logo-divider"></span>
                <span class="fmwa-navbar-title">FEDERAL MINISTRY OF WOMEN AFFAIRS</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Toggle navigation menu" aria-expanded="false">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="index.html" title="Go to home page">Home</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="aboutDropdown" role="button" data-bs-toggle="dropdown" title="Learn about the ministry" aria-expanded="false">
                            About Us
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="aboutDropdown">
                            <li><a class="dropdown-item" href="about.html#mandate-section" title="View our mandate">Mandate</a></li>
                            <li><a class="dropdown-item" href="about.html#mission-section" title="Read our mission">Mission</a></li>
                            <li><a class="dropdown-item" href="about.html#vision-section" title="Learn about our vision">Vision</a></li>
                            <li class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="organogram.html" title="View our organizational structure">Organogram</a></li>
                        </ul>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="departmentsDropdown" role="button" data-bs-toggle="dropdown" title="Explore our departments and divisions" aria-expanded="false">
                            Departments
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="departmentsDropdown">
                            <li><a class="dropdown-item" href="womendevelopment.html" title="Women Development">Women Development</a></li>
                            <li><a class="dropdown-item" href="departments/child-development.html" title="Child Development">Child Development</a></li>
                            <li><a class="dropdown-item" href="departments/community-development-social-intervention.html" title="Community Development & Social Intervention">Community Development & Social Intervention</a></li>
                            <li><a class="dropdown-item" href="departments/gender-affairs.html" title="Gender Affairs">Gender Affairs</a></li>
                            <li><a class="dropdown-item" href="departments/nutrition.html" title="Nutrition">Nutrition</a></li>
                            <li><a class="dropdown-item" href="departments/general-services.html" title="General Services">General Services</a></li>
                            <li><a class="dropdown-item" href="departments/planning-research-statistics.html" title="Planning, Research & Statistics">Planning, Research & Statistics</a></li>
                            <li><a class="dropdown-item" href="departments/finance-accounting.html" title="Finance & Accounting">Finance & Accounting</a></li>
                            <li><a class="dropdown-item" href="departments/procurement.html" title="Procurement">Procurement</a></li>
                            <li><a class="dropdown-item" href="departments/reform-coordination-service-improvement.html" title="Reform Coordination & Service Improvement">Reform Coordination & Service Improvement</a></li>
                            <li class="dropdown-divider"></li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle" href="#" title="Divisions">Divisions</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="#" title="Legal Services">Legal Services</a></li>
                                    <li><a class="dropdown-item" href="#" title="Press Unit">Press Unit</a></li>
                                    <li><a class="dropdown-item" href="#" title="Internal Audit">Internal Audit</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item hidden-nav-item"><a class="nav-link" href="#" title="View our programs">Programs</a></li>
                    <li class="nav-item hidden-nav-item"><a class="nav-link" href="#" title="Read our latest news">News</a></li>
                    <li class="nav-item hidden-nav-item"><a class="nav-link" href="#" title="Contact us">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>`;

// Function to update navigation in a file
function updateNavigationInFile(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Check if this is the index.html file (homepage)
        const isIndex = filePath.endsWith('index.html');
        
        // Check if this is a department page
        const isDepartmentPage = filePath.includes('departments/') || filePath.endsWith('womendevelopment.html');
        
        // Customize navigation based on page type
        let updatedNav = newNavHTML;
        
        // Set active states
        if (isIndex) {
            // For homepage, set Home as active
            updatedNav = updatedNav.replace(
                '<a class="nav-link" href="index.html" title="Go to home page">',
                '<a class="nav-link active" href="index.html" title="Go to home page">'
            );
        } else if (isDepartmentPage) {
            // For department pages, set Departments as active
            updatedNav = updatedNav.replace(
                '<a class="nav-link dropdown-toggle" href="#" id="departmentsDropdown"',
                '<a class="nav-link dropdown-toggle active" href="#" id="departmentsDropdown"'
            );
            
            // Set the specific department as active in the dropdown
            const departmentName = path.basename(filePath, '.html');
            updatedNav = updatedNav.replace(
                `href="${departmentName}.html"`,
                'class="dropdown-item active" href="#"'
            );
        } else if (filePath.endsWith('about.html')) {
            // For about page, set About Us as active
            updatedNav = updatedNav.replace(
                '<a class="nav-link dropdown-toggle" href="#" id="aboutDropdown"',
                '<a class="nav-link dropdown-toggle active" href="#" id="aboutDropdown"'
            );
        } else if (filePath.endsWith('organogram.html')) {
            // For organogram page, set About Us as active
            updatedNav = updatedNav.replace(
                '<a class="nav-link dropdown-toggle" href="#" id="aboutDropdown"',
                '<a class="nav-link dropdown-toggle active" href="#" id="aboutDropdown"'
            );
        }
        
        // Replace the navigation section in the file
        const navRegex = /<nav[\s\S]*?<\/nav>/;
        
        if (navRegex.test(content)) {
            const updatedContent = content.replace(navRegex, updatedNav);
            fs.writeFileSync(filePath, updatedContent, 'utf8');
            console.log(`✅ Updated navigation in ${filePath}`);
            return true;
        } else {
            console.log(`⚠️  No navigation found in ${filePath}`);
            return false;
        }
    } catch (error) {
        console.error(`❌ Error updating ${filePath}:`, error.message);
        return false;
    }
}

// Get all HTML files in the project
getAllHTMLFiles = (dir, fileList = []) => {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
            // Skip node_modules and .git directories
            if (file !== 'node_modules' && !file.startsWith('.') && file !== 'templates') {
                getAllHTMLFiles(filePath, fileList);
            }
        } else if (path.extname(file) === '.html') {
            fileList.push(filePath);
        }
    });
    
    return fileList;
};

// Main function to update all HTML files
const updateAllFiles = () => {
    const htmlFiles = getAllHTMLFiles('.');
    console.log(`Found ${htmlFiles.length} HTML files to update.`);
    
    let successCount = 0;
    
    htmlFiles.forEach(file => {
        if (updateNavigationInFile(file)) {
            successCount++;
        }
    });
    
    console.log(`\n✅ Successfully updated ${successCount} out of ${htmlFiles.length} files.`);
};

// Run the update
updateAllFiles();
