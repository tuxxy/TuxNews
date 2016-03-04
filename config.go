package main

import (
    "gopkg.in/yaml.v2"
    "io/ioutil"
)

type BotConfig struct {
    Server      string  `yaml:"server"`
    Port        string  `yaml:"port"`
    SSL         bool    `yaml:"ssl"`
    IgnoreCert  bool    `yaml:"ignore_cert"`
    Channels    []string   `yaml:"channels,flow"`
    Bot struct {
        Nick        string  `yaml:"nick"`
        User        string  `yaml:"user"`
        Nickserv struct {
            Enabled     bool    `yaml:"enabled"`
            Pass        string  `yaml:"pass"`
            User        string  `yaml:"user"`
            ServName    string  `yaml:"serv_name"`
            ServCommand string  `yaml:"serv_command"`
        }
    }
}

func (c *BotConfig) Init(filename string) error {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }
    if err := yaml.Unmarshal(data, &c); err != nil {
        return err
    }
    return nil
}
