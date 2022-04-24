let watchman = require('fb-watchman');
let client = new watchman.Client();
const {NodeSSH} = require('node-ssh')

const ssh = new NodeSSH()
let dir_of_interest = "/home/conor/University/Project/Pi";

/**
 * Process the arguments to see if we want to automatically restart the program:
 */
const args = process.argv.slice(2);

let restart = true;
if(args[0] !== undefined) {
    restart = false;
}

const password = 'raspberry';

ssh.connect({
    host: 'raspberrypi.local',
    username: 'pi',
    port: 22,
    password,
}).catch((error) => {
    console.log('Failed to connect to server.');
    console.log(error);
}).then(() => {
    client.capabilityCheck(
        {
            optional:[],
            required:['relative_root']
        },
        /**
         * The callback that is called when capability check is complete.
         * @param error
         * @param resp
         */
        function (error, resp) {

            if (error) {
                console.log(error);
                client.end();
                return;
            }

            // Initiate the watch
            client.command(['watch-project', dir_of_interest],

                function (error, resp) {

                    if (error) {
                        console.error('Error initiating watch:', error);
                        return;
                    }

                    // Show any warnings that come up when setting the watch.
                    if ('warning' in resp) {
                        console.log('warning: ', resp.warning);
                    }

                    console.log('watch established on ', resp.watch, ' relative_path', resp.relative_path);

                    // Now, set up the subscription:
                    make_subscription(client, resp.watch, resp.relative_path);

                });
        });
})

function make_subscription(client, watch, relative_path) {
    let sub = {
        // Match any `.py` file in the dir_of_interest
        expression: ["allof", ["match", "*.py"]],
        // Which fields we're interested in
        fields: ["name", "size", "mtime_ms", "exists", "type"]
    };
    if (relative_path) {
        sub.relative_root = relative_path;
    }

    client.command(['subscribe', watch, 'mysubscription', sub],
        function (error, resp) {
            if (error) {
                // Probably an error in the subscription criteria
                console.error('failed to subscribe: ', error);
                return;
            }
            console.log('subscription ' + resp.subscribe + ' established');
        });

    client.on('subscription', function (resp) {
        if (resp.subscription !== 'mysubscription') return;

        resp.files.forEach(function (file) {
            upload_files_to_pi(file)
        });

        if(restart) {
            // Send a request to the Pi to restart the main process:
            ssh.execCommand("python /home/pi/Cycle/restart.py").then((result) => {
                console.log('Updated and restarted.');
            });
        }

    });
}

/**
 * Takes a file and uploads it to the raspberry pi's specified location
 * @param file
 */
function upload_files_to_pi(file)
{
    ssh.putFile(`./${file.name}`, `/home/pi/Cycle/${file.name}`).then(function() {
        console.log(`${file.name} replicated.`);
    }, function(error) {
        console.log("Something's wrong");
        console.log(error)
    });
}