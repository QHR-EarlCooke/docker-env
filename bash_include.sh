# Copyright 2015 Blake Dickie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

if [ -n "$BASH" ]
then
	DOCKERENV_SOURCE="${BASH_SOURCE[0]}"
else
	DOCKERENV_SOURCE="$0"
fi
while [ -h "$DOCKERENV_SOURCE" ]; do
  DOCKERENV_DIR="$( cd -P "$( dirname "$DOCKERENV_SOURCE" )" && pwd )"
  DOCKERENV_SOURCE="$(readlink "$DOCKERENV_SOURCE")"
  [[ $DOCKERENV_SOURCE != /* ]] && DOCKERENV_SOURCE="$DOCKERENV_DIR/$DOCKERENV_SOURCE"
done
DOCKERENV_DIR="$( cd -P "$( dirname "$DOCKERENV_SOURCE" )" && pwd )"

export DOCKERENV_SCRIPT="${DOCKERENV_DIR}/docker-env.py"

function docker-env() {
	eval $(${DOCKERENV_SCRIPT} "$@")
}