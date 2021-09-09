#pragma once

#include <map>
#include <string>

using namespace std;

namespace config
{
    typedef void* (*CreateObjPtr)();

    class ClassFactory
    {
    public:
        void RegisterClass(const string& classname, CreateObjPtr method)
        {
            auto iter = class_map_.find(classname);
            if (iter != class_map_.end())
            {
                return;
            }

            class_map_.insert(pair<std::string, CreateObjPtr>(classname, method));
        }

        void* GetClassByName(const std::string& classname)
        {
            auto iter = class_map_.find(classname);
            if (iter == class_map_.end())
            {
                return nullptr;
            }

            return iter->second();
        }

        static ClassFactory* Instance()
        {
            if (ptr_)
            {
                return ptr_;
            }

            std::call_once(once_flag_, [&]() { ptr_ = new ClassFactory(); });
            return ptr_;
        }

    private:
        map<std::string, CreateObjPtr> class_map_;
        static std::once_flag once_flag_;
        static ClassFactory* ptr_;
    };
    
    std::once_flag ClassFactory::once_flag_;
        
    ClassFactory* ClassFactory::ptr_ = nullptr;

    class RegisterClassAction
    {
    public:
        RegisterClassAction(const string& class_name, CreateObjPtr create_ptr)
        {
            ClassFactory::Instance()->RegisterClass(class_name, create_ptr);
        }
    };

#define REGISTER_REFLECTOR(classname)    \
    classname* ObejctCreate##classname() \
    {                                    \
        return new classname();          \
    }                                    \
    config::RegisterClassAction g_register##classname(#classname, (config::CreateObjPtr)ObejctCreate##classname);

}  // namespace config