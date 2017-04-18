var spawn = require('child_process').spawn;

require('dotenv').config();
var _ = require('lodash');
var yargs = require('yargs');
var validator = require('validator');

var remotes = require('./remotes');
var commandChecks = require('./helpers/command/check');

var ENV_PREFIX = 'STAX_ATTACK';

var argumentOptions = {
  n: {
    alias: 'name',
    describe: 'Name of the test run',
    default: 'Default test name',
    type: 'string'
  },
  t: {
    alias: 'title',
    describe: 'Description of the test run',
    default: 'Default test description',
    type: 'string'
  },
  r: {
    alias: 'remote',
    describe: 'Which remote service to use?  Leave out to run locally.',
    // choices are remotes as defined in ./tests/remotes.js, and can also be false for running locally.
    choices: _.concat(_.keys(remotes), false)
  },
  p: {
    alias: 'project',
    describe: 'Which project are you testing?',
    default: 'tutor',
    choices: commandChecks.getValidProjects()
  },
  c: {
    alias: 'cases',
    describe: 'Which case ids are you running?',
    type: 'array'
  },
  b: {
    alias: 'browsers',
    default: [
      'safari'
      //'chrome:36:Windows',
      //'firefox:36:Windows',
      // 'internet explorer:10:Windows 7'
    ],
    describe: 'What browsers should the tests run in?',
    type: 'array'
  },
  s: {
    alias: 'server',
    describe: 'What server should the tests run against?',
    default: 'qa'
  }
};

function buildTestOptions(){
  var argv = yargs.usage('Usage: $0 ')
    .env(ENV_PREFIX)
    .config('settings')
    .options(argumentOptions)
    .example('c', '$0 -c 7651 7674', 'Run tests for cases 7651 and 7674.')
    .help('h')
    .alias('h', 'help')
    .check(commandChecks.checkArgs)
    .argv;

  var remoteName = argv.r;
  var optionsForMocha = getOptionsForMocha(argv);
  var isEnvOurs = _.partial(commandChecks.isEnvOurs, ENV_PREFIX);

  var envs = _.pickBy(process.env, isEnvOurs);
  var systemEnvs = _.omitBy(process.env, isEnvOurs);
  var remoteEnvs;

  envs.SELENIUM_CAPABILITIES = {name: argv.name};
  if(commandChecks.isRemote(argv)){
    remoteEnvs = remotes[remoteName].buildEnvs(envs);
    remotes[remoteName].cleanEnvs(envs);
    _.defaultsDeep(envs, remoteEnvs);
  }
  envs.SELENIUM_CAPABILITIES = JSON.stringify(envs.SELENIUM_CAPABILITIES);
  envs.SERVER_URL = commandChecks.getServerUrlFromArgs(argv);

  var envsFromArgs = buildEnvFromArgs(_.pick(argv, ['cases', 'project', 'title']));

  _.defaults(envs, envsFromArgs);
  _.extend(envs, systemEnvs);

  var testEnvs = _.map(argv.browsers, function(browser){
    return buildBrowserEnv(envs, browser);
  });

  return {
    browsers: argv.browsers,
    envs: testEnvs,
    system: envs.SELENIUM_REMOTE_URL || 'local',
    cases: JSON.parse(envs.STAX_ATTACK_CASES),
    runName: argv.name,
    additionalOptions: optionsForMocha,
    serverUrl: envs.SERVER_URL
  };
}

function getOptionsForMocha(argv, seleniumAndEnvOptions){
  var unlistedOptions = ['_', 'h', 'help', 'settings', '$0'];
  var seleniumAndEnvOptions = _(argumentOptions).keys().concat(_.map(argumentOptions, _.property('alias')), unlistedOptions).value();

  var otherOptions = _.omit(argv, seleniumAndEnvOptions);
  var optionsForMocha = _.flatMap(otherOptions, function(value, key){
    var prefix = '-';
    if(key.length > 1){
      prefix += '-';
    }
    var option = [prefix + key];
    if(_.isString(value)){
      option.push(value);
    }

    return option;
  });

  return optionsForMocha;
}

function buildEnvFromArgs(args){
  var envs = {};
  _.each(args, function(arg, argName){
    var envArgName = _.chain(ENV_PREFIX + ' ' + argName).snakeCase().toUpper().value();
    if(!_.isString(arg)){
      arg = JSON.stringify(arg);
    }
    envs[envArgName] = arg;
  });

  return envs;
}

function buildBrowserEnv(baseEnv, browser){
  return _.extend({}, baseEnv, {SELENIUM_BROWSER: browser, STAX_ATTACK_TITLE: _.capitalize(browser) + ' | ' +  baseEnv.STAX_ATTACK_TITLE});
}

function buildReportInfo(testOptions){
  var browsers = testOptions.browsers.join(', ');
  var cases = testOptions.cases.join(', ');

  return 'Running ' + testOptions.runName + ' with cases ' + cases + ' on browsers ' + browsers + ' at ' + testOptions.system + ' on ' + testOptions.serverUrl;
}

function runTests(){
  var testOptions = buildTestOptions();
  var childCommand = _.concat(['-R', 'spec'], testOptions.additionalOptions, './pre-run.js');

  process.stdout.write(buildReportInfo(testOptions));

  var mochas = _.map(testOptions.envs, function(env){
    return spawn('mocha', childCommand, {stdio: "inherit", env: env});
  });
}

runTests();
