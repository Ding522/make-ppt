-- render_ppt_mac.applescript <deck.pptx> <output.pdf>
-- Uses PowerPoint for macOS to preserve the layout before PNG conversion.
on run argv
    if (count of argv) is not 2 then error "Expected input PPTX and output PDF paths"

    set inputPath to item 1 of argv
    set outputPath to item 2 of argv
    set openedPresentation to missing value

    tell application "Microsoft PowerPoint"
        launch
        try
            open inputPath
            set openedPresentation to active presentation
            save openedPresentation in outputPath as save as PDF
            close openedPresentation saving no
        on error errorMessage number errorNumber
            if openedPresentation is not missing value then
                try
                    close openedPresentation saving no
                end try
            end if
            error errorMessage number errorNumber
        end try
    end tell

    return outputPath
end run
