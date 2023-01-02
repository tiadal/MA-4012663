module.exports = function(grunt) {
    grunt.initConfig({
        uncss: {
            dist: {
                files: [{
                    nonull: true,
                    src: ['http://127.0.0.1:8000/create/settings/form/2'],
                    dest: 'styles2.css'
                }]
            }, 
            options: {
                ignoreSheets : [/fonts.googleapis/, /cdn.jsdelivr.net/],
                stylesheets: ['https://storage.googleapis.com/mabtu/app/main.css'],
            }
        }
    });

    // Load the plugins
    grunt.loadNpmTasks('grunt-uncss');

    // Default tasks.
    grunt.registerTask('default', ['uncss']);

};