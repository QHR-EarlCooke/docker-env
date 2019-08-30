# docker-env

A set of scripts to help manage connecting to different docker instances which use **TLS** to authenticate.

## Usage

`docker-env [--env=<ENVNAME>] [machine_name]`

The `--env` property defines with environment to run against.  If it is not provided, the last envrionment used for the current shell
session will be used.  If no enviornment has been used yet, `develop` will be used.

If a `machine_name` is pasted then the current shell environment will be configured to connect to the machine with
the matching definition in the environment's `machines.json` file.

If no `machine_name` is pasted the a list of the machines in the current environment will be printed.

It is recommended to include a full call to `docker-env` including `--env` and your perferred default `machine_name`
if your shell's startup files to ensure your environment is always valid for new shell sessions.

## Setup

### Bash Shell

1. Clone docker-env to a local directory.  This checkout location will be referred to as `<CHECKOUT>` for the following steps.
2. In `$HOME/.bashrc` or `$HOME/.bash_profile` add `source <CHECKOUT>/bash_include.sh`.
3. Setup the `DOCKER_ENV_PROFILES` envrionment variable to point to your environment definition folder (see below).

## Environment Definitions

An environment refers to a set of docker instances that all share a single certificate authority.  The environments and machines are defined in a folder.

For each environment:

1. Create a sub-folder with the name of the environment and all the rest of the files to it.
2. Put the CA public certificate as `ca.crt`.
3. Put the user's client certificate and key as `personal.crt` and `personal.key` respectively.
4. Create a `machines.json` file listing the docker instances within the environment.

### machines.json Format

The machines.json file should contain an entry for each environment with the name of the environment as the key.  The host property should contain the
IP address or hostname for connecting to the environment.  The port property should contain the port to connect to.

```json
{
  "local": {
    "host": "127.0.0.1",
    "port": "2376"
  },
  
  "sandbox": {
    "host": "192.168.1.20",
    "port": "2376"
  }
}
```
