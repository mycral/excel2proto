package config

import (
	"errors"
	"fmt"
)

type StringToStructFunc func() interface{}

type StringToStructMgr struct {
	funcs map[string]StringToStructFunc
}

func NewStringToStructMgr() *StringToStructMgr {
	return &StringToStructMgr{
		funcs: make(map[string]StringToStructFunc),
	}
}

func (s *StringToStructMgr) Register(str string, strToStructFunc StringToStructFunc) error {
	if _, ok := s.funcs[str]; !ok {
		s.funcs[str] = strToStructFunc
		return nil
	}

	return errors.New(fmt.Sprintf("%v Exist", str))
}

func (s *StringToStructMgr) GetStructObj(str string) interface{} {
	if strToStructFunc, ok := s.funcs[str]; ok {
		return strToStructFunc()
	}
	return nil
}

var GStringToStructMgr *StringToStructMgr

func init() {
	GStringToStructMgr = NewStringToStructMgr()
}
