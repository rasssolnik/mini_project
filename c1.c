int main(int argc, char **argv)
{
    char flags[7] = "\0";
    int index_end_flags = 1;
    flags_parser(flags, argc, argv, &index_end_flags);

    // если не было подано файла
    if (index_end_flags == arg_count - 1)
        print_file("-", flags);

    for (int i = index_end_flags + 1; i < argc, i++)
    {
        if (strcmp(args[i], "--") == 0)
            continue;
        print_file(argv[i], flags);
    }
    return 0;
}

int print_file(char *name, char *flags)
{
    int err_code = 0;
    FILE *f;
    // если имя файла "-" работаем с stdin
    if (strcmp("-", name) == 0)
        f = stdin;
    else
        f = fopen(name, "rt");

    if (f != NULL)
    {
        int index = 0;
        bool eline_printed = 0;
        int c = fgetc(f), prev = '\n';
        while (c != EOF)
        {
            print_symb(c, &prev, flags, &index, &eline_printed);
            c = fgetc(f);
        }
        if (f != stdin)
            fclose(f); // закрываем файл только если он не stdin
    }
    else
    {
        err_code = 1;
    }
    return err_code;
}
