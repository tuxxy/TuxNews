package main

import (
    "crypto/tls"
    irc "github.com/fluffle/goirc/client"
    "fmt"
)

type Bot struct {
    Client  *irc.Conn
    Config  *BotConfig
}

func (b *Bot) NewBot(c *BotConfig) *Bot {
    cfg := *irc.NewConfig(c.Bot.Nick)
    cfg.Me.Ident = c.Bot.User
    cfg.Me.Name = "TuxNews v1.0"
    if c.SSL {
        cfg.SSL = true
        cfg.SSLConfig = &tls.Config{ServerName: c.Server,
            InsecureSkipVerify: c.IgnoreCert}
    } else {
        cfg.SSL = false
    }
    cfg.Server = c.Server + ":" + c.Port
    cfg.Version = "TuxNews v1.0 - https://github.com/tuxxy/TuxNews"
    
    Client := *irc.Client(&cfg)
    

    return &Bot{Client: &Client, Config: c}
}

func (b *Bot) Connect() {
	fmt.Println("Connecting to server...")
    if err := b.Client.Connect(); err != nil {
        panic(err)
    }
}
