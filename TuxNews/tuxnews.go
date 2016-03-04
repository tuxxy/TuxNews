package main

type TuxNews struct {
    Config  *BotConfig
}

func (t *TuxNews) Init(c *BotConfig) *TuxNews {
    return &TuxNews{Config: c}
}
